# This file defines a base class (protocol) that all agents must follow.
# Ensures every agent implements the same set of required methods like act().
# Useful for enforcing structure and consistency across different agents.

from typing import Protocol, List, Any, Dict

class AgentProtocol(Protocol):
    def get_response(self, messages: List[Dict[str, Any]]) -> Dict[str,Any]:
        ...