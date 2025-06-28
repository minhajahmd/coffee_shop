from openai import OpenAI
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response, double_check_json_output
import dotenv
dotenv.load_dotenv()

class GuardAgent():
    # This agent checks if the user is asking something relevant to the coffee shop or not.

    def __init__(self):
        self.client= OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME") 

    def get_response(self, messages): 
        messages = deepcopy(messages)
        system_prompt = """
            You are a helpful assistant for a coffee shop application which serves drinks and pastries.
            Your task is to determine if the user is asking something relevant to the coffee shop or not.
            The user is allowed to:
            1. Ask questions about the coffee shop, like location, working hours, menu items, and coffee shop related questions.
            2. Ask questions about menu items, like ingredients in an item and more details about the item.
            3. Make an order.
            4. Ask about the recommendations of what to buy.

            The user is not allowed to:
            1. Ask questions that are not related to the coffee shop.
            2. Ask questions about the staff or how to make a certain menu item.       

            ✅ Format your output as **valid JSON**, exactly like this:            
            {
                "chain of thought": "go over each of the points above and see if the message lies under this point or not. Then you write some thoughts about what point is this input relevant to."
                "decision": "allowed" or "not allowed". Pick one of those and only write the word.
                "message": leave the message empty "" if it's allowed, otherwise write "Sorry, I cannot help with that. Can I help you with your order?"
            }
        """ 
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]  # Use the last 3 messages to provide context

        chatbot_output = get_chatbot_response(
            self.client, 
            self.model_name, 
            input_messages
            )
        print("Guard Agent Output:", chatbot_output)
        chatbot_output = double_check_json_output(self.client, self.model_name, chatbot_output)
        output = self.postprocess(chatbot_output)

        return output
    
    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {
                "agent": "guard_agent",
                "guard_decision": output['decision']
            }
        }
        return dict_output