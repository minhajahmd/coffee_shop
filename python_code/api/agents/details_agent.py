from dotenv import load_dotenv
import os
from openai import OpenAI
from .utils import get_chatbot_response, get_embedding
from copy import deepcopy
from pinecone import Pinecone
load_dotenv()

class DetailsAgent():
    # This agent provides details about the coffee shop, like location, working hours, menu items, etc.
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME")
        self.embedding_client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_EMBEDDING_URL")
        )
        self.pc = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY")
        )
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

    def get_closest_results(self, index_name, input_embeddings, top_k=2):
        index = self.pc.Index(index_name)

        results = index.query(
            namespace='ns1',
            vector=input_embeddings,
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )
        return results
    
    def get_response(self, messages):
        messages = deepcopy(messages)

        user_message = messages[-1]['content'] # Get the last user message
        embeddings = get_embedding(self.embedding_client, self.model_name, user_message)[0] # Get the embedding for the user message
        result = self.get_closest_results(self.index_name, embeddings) # Get the closest results from Pinecone
        source_knowledge = '\n'.join([x['metadata']['text'].strip()+ '\n' for x in result['matches']]) # Join the texts from the closest results

        # One liner loops for the above 
        #    squares = []                               
        #    for x in range(5):           ====>>>           squares = [x * x for x in range(5)]
        #       squares.append(x * x)


        prompt = f"""
            Using the contexts below, answer the user's query:

            Contexts:
            {source_knowledge}
            Query:
            {user_message}
        """

        system_prompt = """
            You are a customer support agent for a coffee shop called Velvet Hours. You should answer every question as if you are a waiter and provide the necessary information to the user regarding the orders.
            """
        messages[-1]['content'] = prompt  # Replace the last user message with the prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:] # Use the last 3 messages to provide context

        chatbot_output = get_chatbot_response(
            self.client, 
            self.model_name, 
            input_messages
        )
        output = self.postprocess(chatbot_output)
        return output
    
    def postprocess(self, output):
        output = {
            "role": "assistant",
            "content": output,
            "memory": {
                "agent": "details_agent"
            }
        }
        return output