from openai import OpenAI
import pandas as pd
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response, double_check_json_output
import dotenv
dotenv.load_dotenv()

class RecommendationAgent():
    # This agent provides recommendations to the user about what to buy based on their preferences.
    def __init__(self, apriori_recommendation_path, popular_recommendation_path):
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME")

        with open(apriori_recommendation_path, 'r') as file:    # Load the apriori recommendations from a JSON file
            self.apriori_recommendations = json.load(file)      # This file contains a dictionary where each key is a product and the value is a list of recommendations for that product

        self.popular_recommendations = pd.read_csv(popular_recommendation_path)    # Load the popular recommendations from a CSV file

        self.products = self.popular_recommendations['product'].tolist()   # List of all products in the popular recommendations
        self.product_categories = list(set(self.popular_recommendations['product_category'].tolist()))  # List of all product categories in the popular recommendations

    def get_apriori_recommendations(self, products, top_k=5):
        recommendation_list = []  # Initialize an empty list to store recommendations

        for product in products:  # Iterate through each product in the input list
            if product in self.apriori_recommendations:  # Check if the product has recommendations
                recommendation_list += self.apriori_recommendations[product]  # Add the recommendations (with product, product_category, and confidence) to the recommendation list
        
        recommendation_list = sorted(recommendation_list, key=lambda x: x['confidence'], reverse=True)  # Sort the recommendations by their confidence score in descending order
        
        recommendations =  []  # Initialize an empty list to store the final recommendations
        recommendations_per_category = {}  # Dictionary to keep track of recommendations per category
        for recommendation in recommendation_list:  # Iterate through the sorted recommendations
            if recommendation in recommendations:   # If the recommendation is already in the final list, skip it
                continue 

            # Limit 2 recommendations per category because we want to avoid recommending too many products from the same category
            product_category = recommendation['product_category']
            if product_category not in recommendations_per_category:    # If the category is not in the dictionary, initialize it
                recommendations_per_category[product_category] = 0 
            
            if recommendations_per_category[product_category] >= 2:     # If the category already has 2 recommendations, skip this one
                continue

            recommendations_per_category[product_category] += 1  # Increment the count for the category

            recommendations.append(recommendation['product'])  # Add the product to the final recommendations list

            if len(recommendations) >= top_k:  # If we have enough recommendations, break the loop
                break
        return recommendations  # Return the final list of recommendations


    def get_popular_recommendations(self, product_categories=None, top_k=5):
        recommendation_df = self.popular_recommendations # Start with the full DataFrame of popular recommendations

        if product_categories is not None:      # If product categories are provided, filter the DataFrame to include only those categories
            recommendation_df = self.popular_recommendations[self.popular_recommendations['product_category'].isin(product_categories)]
        recommendation_df = recommendation_df.sort_values('number_of_transactions', ascending=False) # Sort the DataFrame by the number of transactions in descending order

        if recommendation_df.shape[0]==0:
            return "Sorry, we don't have any recommendations for that category."
        
        recommendations = recommendation_df['product'].tolist()[:top_k]   # Get the top K recommendations from the sorted DataFrame
        return recommendations

        # Now we need to classify the type of recommendation based on the user's query.
        #   "What do people usually get with a croissant?" → Apriori
        #   "What's popular these days?" → Popular
        #   "What coffee would you recommend?" → Popular by category

    def recommendation_classification(self, messages):
        system_prompt = f""" You are a helpful AI assistant for a coffee shop application which serves drinks and pastries. We have 3 types of recommendations:

        1. Apriori Recommendations: These are recommendations based on the user's order history. We recommend items that are frequently bought together with the items in the user's order.
        2. Popular Recommendations: These are recommendations based on the popularity of items in the coffee shop. We recommend items that are popular among customers.
        3. Popular Recommendations by Category: Here the user asks to recommend them product in a category. Like what coffee do you recommend me to get?. We recommend items that are popular in the category of the user's requested category.
        
        Here is the list of items in the coffee shop:
        """+ ",".join(self.products) + """
        Here is the list of Categories we have in the coffee shop:
        """ + ",".join(self.product_categories) + """

        Your task is to determine which type of recommendation to provide based on the user's message.

        Your output should be in a structured json format like so. Each key is a string and each value is a string. Make sure to follow the format exactly:
        {
        "chain of thought": Write down your critical thinking about what type of recommendation is this input relevant to.
        "recommendation_type": "apriori" or "popular" or "popular by category". Pick one of those and only write the word.
        "parameters": This is a python list. It's either a list of of items for apriori recommendations or a list of categories for popular by category recommendations. Leave it empty for popular recommendations. Make sure to use the exact strings from the list of items and categories above.
        }
        """

        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]  # Use the last 3 messages to provide context

        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)
        chatbot_output = double_check_json_output(self.client, self.model_name, chatbot_output)  # Double check the output to make sure it's a valid JSON string
        output = self.postprocess_classification(chatbot_output)

        return output

    def postprocess_classification(self, output):
        output = json.loads(output)

        dict_output = {
            "recommendation_type": output['recommendation_type'],
            "parameters": output['parameters'],
        }
        return dict_output


    def get_recommendations_from_order(self, messages, order):
        messages = deepcopy(messages)
        products= []
        for product in order:
            products.append(product['item'])    # Extract the item from each order in the order list 

        recommendations = self.get_apriori_recommendations(products)    # If the user has ordered items, get the apriori recommendations for those items
        recommendations_str = ', '.join(recommendations)        # Convert list to comma-separated string

        system_prompt = f"""
        You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
        your task is to recommend items to the user based on their order.

        I will provide what items you should recommend to the user based on their order in the user message. 
        """
    
        prompt = f"""
        {messages[-1]['content']}

        Please recommend me those items correctly: {recommendations_str}
        """

        messages[-1]['content'] = prompt  # Replace the last user message with the prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)
        output = self.postprocess_recommendation(chatbot_output)

        return output
    
    def get_response(self, messages):       
        # This is the main function that gets called by the Classification Agent to get recommendations based on the user's input.
        
        messages = deepcopy(messages)

        recommendation_classification = self.recommendation_classification(messages)
        recommendation_type = recommendation_classification['recommendation_type']

        recommendations= []
        if recommendation_type == "apriori":
            recommendations = self.get_apriori_recommendations(recommendation_classification['parameters'])
        elif recommendation_type == "popular":
            recommendations = self.get_popular_recommendations()
        elif recommendation_type == "popular by category":
            recommendations = self.get_popular_recommendations(recommendation_classification['parameters'])

        if recommendations == []:
            return {"role": "assistant", "content": "Sorry, we don't have any recommendations for that. Can I help you with something else?"}

        # Respond to User
        recommendations_str = ', '.join(recommendations)
        
        system_prompt = f"""
        You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
        your task is to recommend items to the user based on their input message. And respond in a friendly but concise way. And put it an unordered list with a very small description.

        I will provide what items you should recommend to the user based on their order in the user message. 
        """

        prompt = f"""
        {messages[-1]['content']}
        Please recommend me those items correctly: {recommendations_str}
        """
        messages[-1]['content'] = prompt  # Replace the last user message with the prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]
        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)
        output = self.postprocess_recommendation(chatbot_output)
        return output

    def postprocess_recommendation(self, output):
        output = {
            "role": "assistant",
            "content": output,
            "memory": {
                "agent": "recommendation_agent"
            }
        }
        return output
