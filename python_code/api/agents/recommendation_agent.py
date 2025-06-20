from openai import OpenAI
import pandas as pd
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response
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
            self.apriori_recommendations = json.load(file)

        self.popular_recommendations = pd.read_csv(popular_recommendation_path)    # Load the popular recommendations from a CSV file

        self.products = self.popular_recommendations['product'].tolist()   # List of all products in the popular recommendations
        self.product_categories = self.popular_recommendations['product_category'].tolist()  # List of all product categories in the popular recommendations


    def get_popular_recommendations(self, product_categories=None, top_k=5):
        recommendation_df = self.popular_recommendations # Start with the full DataFrame of popular recommendations

        if product_categories is not None:      # If product categories are provided, filter the DataFrame to include only those categories
            recommendation_df = self.popular_recommendations[self.popular_recommendations['product_category'].isin(product_categories)]
        recommendation_df = recommendation_df.sort_values('number_of_transactions', ascending=False) # Sort the DataFrame by the number of transactions in descending order

        if recommendation_df.shape[0]==0:
            return "Sorry, we don't have any recommendations for that category."
        
        recommendations = recommendation_df['product'].tolist()[:top_k]   # Get the top K recommendations from the sorted DataFrame
        return recommendations
