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
            self.apriori_recommendations = json.load(file)      # This file contains a dictionary where each key is a product and the value is a list of recommendations for that product

        self.popular_recommendations = pd.read_csv(popular_recommendation_path)    # Load the popular recommendations from a CSV file

        self.products = self.popular_recommendations['product'].tolist()   # List of all products in the popular recommendations
        self.product_categories = self.popular_recommendations['product_category'].tolist()  # List of all product categories in the popular recommendations

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
