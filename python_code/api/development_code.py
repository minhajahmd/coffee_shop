# Sandbox/testing file to prototype agent behavior and run experiments.
# Not part of production — useful for local testing and quick debugging.

from agents import (GuardAgent, ClassificationAgent, DetailsAgent, AgentProtocol, RecommendationAgent, OrderTakingAgent)
import os
from typing import Dict
import pathlib
folder_path = pathlib.Path(__file__).parent.resolve()


def main():
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    recommendation_agent = RecommendationAgent(
            os.path.join(folder_path, 'recommendation_objects/apriori_recommendation.json'),
            os.path.join(folder_path, 'recommendation_objects/popularity_recommendation.csv')
        )

    agent_dict: Dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "recommendation_agent": recommendation_agent,
        "order_taking_agent": OrderTakingAgent(recommendation_agent)
    }

    messages = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n Guard Agent is running.")
        for message in messages:
            print(f"{message['role']}: {message['content']}")

        # Get user input
        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})

        # Get Guard Agent's response    
        guard_agent_response = guard_agent.get_response(messages)
        if guard_agent_response['memory']["guard_decision"] == "not allowed":
            messages.append(guard_agent_response)
            continue

        # Get Classifier Agent's response
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent = classification_agent_response['memory']["classification_decision"]

        # Get the chosen agent's response
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)
        messages.append(response)

# Run the script only if it's executed directly (not imported elsewhere)
if __name__ == "__main__":
    main()

