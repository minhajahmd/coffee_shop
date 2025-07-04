from agent_controller import AgentController
import runpod


def main():
    agent_controller = AgentController()
    runpod.serverless.start({"handler": agent_controller.get_response})     # Start the serverless function with the agent controller's response handler


if __name__ == "__main__":
    main()