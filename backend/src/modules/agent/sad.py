import json
import logging

from copy import deepcopy

from backend.src.modules.retrieve.semantic_search import SemanticSearch
from backend.src.utils.response import get_chat_response, get_client
from backend.src.config.app_config import Config as cfg


class SadAgent:
    def __init__(self):
        self.client = get_client(
            api_key=cfg.OPENAI_API_KEY
        )

        self.semantic_search = SemanticSearch()

        logging.info('Initialize Sad Agent ...')

    
    def post_process(self, output):
        output = {
            "role": "assistant",
            "content": output,
            "memory": {
                "agent": "sad_agent"
            }
        }

        return output
    

    def get_response(self, messages):
        messages = deepcopy(messages)
        user_message = messages[-1]["content"]

        relevant_chunks = self.semantic_search.retrieve_relevant_chunks(
            query=user_message
        )

        prompt = f"""
            Using the contexts below
        """

