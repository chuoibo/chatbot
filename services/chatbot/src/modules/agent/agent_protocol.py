from typing import Protocol

class AgentProtocol(Protocol):
    def get_response(self, history, messages):
        ...