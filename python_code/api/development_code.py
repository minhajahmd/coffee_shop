# Sandbox/testing file to prototype agent behavior and run experiments.
# Not part of production — useful for local testing and quick debugging.

from agents import (GuardAgent)
import os

def main():
    pass

# Run the script only if it's executed directly (not imported elsewhere)
if __name__ == "__main__":
    guard_agent = GuardAgent()

    messages = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Guard Agent is running.")
        for message in messages:
            print(f"{message['role']}: {message['content']}")

        # Get user input
        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})

        # Get Guard Agent's response    
        guard_agent_response = guard_agent.get_response(messages)
        if guard_agent_response['memory']["guard_decision"] == "allowed":
            messages.append(guard_agent_response)
            continue

        # Get Classifier Agent's response
