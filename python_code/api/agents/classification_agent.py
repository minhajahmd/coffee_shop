from openai import OpenAI
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response
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
            You are a helpful AI assistant for a coffee shop application.
            Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
            1. details_agent: This agent is responsible for answering questions about the coffee shop, like location, delivery places, working hours, details about menu items. Or listing items in the menu items. Or asking what we have.
            2. order_taking_agent: This agent is responsible for taking orders from the user. It responsible to have a conversation with the user about the order until the order is complete.
            3. recommendation_agent: This agent is responsible for giving recommendations to the user about what to buy. If the user asks for a recommendation, this agent should handle the request.
            
            Your output should be in a structured JSON format like so. Each key is a string and each value is a string. Make sure you follow the format exactly:
            {
                "chain of thought": "go over each of the agents above and write some of your thoughts about what agent in this input relevant to",
                "decision": "details_agent" or "order_taking_agent" or "recommendation_agent". Pick one of those and only write the word,
                "message": leave the message empty
            }
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
            "content": output["message"],
            "memory": {
                "agent": "classification_agent",
                "classification_decision": output["decision"]
            }
        }
        return dict_output