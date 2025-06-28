from openai import OpenAI
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response, double_check_json_output
import dotenv
dotenv.load_dotenv()

class ClassificationAgent():
    # This agent classifies the user input into one of the three agents:
        # 1. details_agent: For questions about the coffee shop, location, menu items, etc.
        # 2. order_taking_agent: For taking orders from the user.
        # 3. recommendation_agent: For giving recommendations to the user about what to buy.

    def __init__(self):
        self.client= OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME") 

    def get_response(self, messages):
        messages = deepcopy(messages)
         
        system_prompt = """
        You are a classification assistant in a multi-agent coffee shop chatbot system.

        💼 Your job is ONLY to classify the user's message and route it to the correct agent.
        ⛔️ You MUST NOT respond like a barista, order-taker, or assistant. You only return classification data.

        You must choose ONE of the following agents:
        1. details_agent — Use this for questions about the coffee shop, like location, hours, delivery, and menu info.
        2. order_taking_agent — Use this if the user wants to place an order, modify it, or add items.
        3. recommendation_agent — Use this if the user is asking what to buy or looking for suggestions.

        ✅ Format your output as **valid JSON**, exactly like this:
        {
        "chain of thought": "Reason about which agent should handle this input and why.",
        "decision": "details_agent" or "order_taking_agent" or "recommendation_agent",
        "message": ""  // This should always be empty
        }

        Return ONLY the JSON above. Do not generate any explanation or assistant-style replies.
        """


        input_messages = [{"role": "system", "content": system_prompt}]
        input_messages += messages[-3:]
        # Use the last 3 messages to provide context

        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)

        output = self.postprocess(chatbot_output)
        return output

    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {
                "agent": "classification_agent",
                "classification_decision": output['decision']
            }
        }
        return dict_output