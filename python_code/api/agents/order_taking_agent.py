import os 
import json
from .utils import get_chatbot_response, double_check_json_output
from openai import OpenAI
from copy import deepcopy
from dotenv import load_dotenv
load_dotenv()

class OrderTakingAgent():
    # This agent is responsible for taking orders from the user. It handles the conversation with the user about the order until the order is complete.
    
    def __init__(self, recommendation_agent):
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME")
        self.recommendation_agent = recommendation_agent  # This is the recommendation agent that will be used to recommend items to the user if they ask for recommendations.

    def get_response(self, messages):
        messages = deepcopy(messages)
        system_prompt = """
            You are a customer support Bot for a coffee shop called "Velvet Hours"

            Here is the MENU for this coffee shop:

            Cappuccino - $4.50
            Jumbo Savory Scone - $3.25
            Latte - $4.75
            Chocolate Chip Biscotti - $2.50
            Espresso shot - $2.00
            Hazelnut Biscotti - $2.75
            Chocolate Croissant - $3.75
            Dark chocolate (Drinking Chocolate) - $5.00
            Cranberry Scone - $3.50
            Croissant - $3.25
            Almond Croissant - $4.00
            Ginger Biscotti - $2.50
            Oatmeal Scone - $3.25
            Ginger Scone - $3.50
            Chocolate syrup - $1.50
            Hazelnut syrup - $1.50
            Carmel syrup - $1.50
            Sugar Free Vanilla syrup - $1.50
            Dark chocolate (Packaged Chocolate) - $3.00

            Things to NOT DO:
            * DON't ask how to pay by cash or Card.
            * Don't tell the user to go to the counter
            * Don't tell the user to go to place to get the order


            You're task is as follows:
                1. Take the User's Order
                2. Validate that all their items are in the menu
                3. If an item is not in the menu let the user and repeat back the remaining valid order
                4. Ask them if they need anything else.
                5. If they do then repeat starting from step 3
                6. If they don't want anything else, do the following using the "order" object:
                    a. First, list down all the items ordered in this format: 
                        - <quantity> x <item name>: $<price>
                        For example: 2 x Latte: $9.50
                    b. After listing all items, calculate and clearly display the total amount.
                    c. Then, thank the user for the order and close the conversation with no more questions.

            The user message will contain a section called memory. This section will contain the following:
            "order"
            "step_number"
            Please utilize this information to determine the next step in the process.
            
        You MUST produce the output in the **exact structured JSON format** below. 
        ⚠️ Absolutely nothing should be added before or after the JSON. 
        ⚠️ All four keys are MANDATORY — never skip any key, even if some values are empty.
        

        Your output MUST follow below format exactly and each key must use **snake_case**. Do NOT use any spaces in the keys:
        {
        "chain_of_thought": "Explain which step the user is currently on, how their message relates to the coffee shop ordering process, and how you will respond — making sure to follow the 'Things to NOT DO' section strictly.",
        "step_number": "Write the current step number as a string. Only the number, no extra text.",
        "order": [
            {
            "item": "<exact item name from menu>",
            "quantity": "<number as string or digit>",
            "price": "<total price for that item as a string, like '4.50'>"
            },
            ...
        ],
        "response": "Write a polite, helpful message to the user based on the current situation. Do not include emojis or questions unless asking if they need anything else. Add the order summary and total amount if the order is complete."
        }

        ✅ Every key in the JSON must appear.
        ✅ If the order is empty, still include the "order": [] key with an empty list.
        ❌ Do NOT return markdown (no triple backticks).
        ❌ Do NOT add commentary or explanation outside the JSON block.
        ❌ Do NOT rephrase the format or wrap in code blocks.

        """

        last_order_taking_status = ""   
        asked_recommendation_before = False        
        # Find the last order taking status from the messages
        # We will look for the last message from the assistant that has the memory of order_taking_agent
        # and extract the step_number and order from it.
        for message in reversed(messages):
            if message["role"] == "assistant" and message.get("memory", {}).get("agent") == "order_taking_agent":
                step_number = message["memory"].get("step_number", "")
                order = message["memory"].get("order", [])
                asked_recommendation_before = message["memory"].get("asked_recommendation_before", False)
                if order:       
                    last_order_taking_status = f"""step_number: {step_number}\norder: {order}"""    
                    break


        messages[-1]['content'] = last_order_taking_status + "\n" + messages[-1]['content']     # Add the last order taking status to the last message content
        input_messages = [{"role": "system", "content": system_prompt}] + messages

        chatbot_response = get_chatbot_response(self.client, self.model_name, input_messages)
        chatbot_response = double_check_json_output(self.client, self.model_name, chatbot_response)

        output = self.postprocess(chatbot_response, messages, asked_recommendation_before)
        return output
    
    def postprocess(self, output, messages, asked_recommendation_before):
        output = json.loads(output)

        if type(output['order'])== str:
            output['order'] = json.loads(output['order'])

        response = output['response']
        if not asked_recommendation_before and len(output['order']) > 0:
            recommendation_output = self.recommendation_agent.get_recommendations_from_order(messages, output['order'])
            response = recommendation_output['content']
            asked_recommendation_before = True

        dict_output = {
            "role": "assistant",
            "content": response,
            "memory": {
                "agent": "order_taking_agent",
                "step_number": output['step_number'],
                "asked_recommendation_before": asked_recommendation_before,
                "order": output['order']
            }
        }
        return dict_output

