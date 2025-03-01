import logging

from copy import deepcopy

from src.modules.retrieve.semantic_search import SemanticSearch
from src.utils.response import get_chat_response, get_client, get_user_intent
from src.config.app_config import Config as cfg


class StoryAgent:
    def __init__(self):
        self.client = get_client(
            api_key=cfg.OPENAI_API_KEY
        )

        self.semantic_search = SemanticSearch()

        logging.info('Initialize Sad Agent ...')

    
    def postprocess(self, output):
        output = {
            "role": "assistant",
            "content": output,
            "memory": {
                "agent": "sad_agent"
            }
        }

        return output
    

    def get_response(self, history, messages):
        messages = deepcopy(messages)

        relevant_chunks = self.semantic_search.retrieve_relevant_chunks(
            query=messages
        )

        user_intent = get_user_intent(
            client=self.client,
            history=history,
            message=messages
        )
        
        prompt = f"""
        You are a compassionate and empathetic guide, dedicated to helping people overcome sadness, fear, and feelings of being lost or discouraged. 
        Your role is not just to provide advice but to **heal through storytelling**. 

        Given latest user message, deeply understand their emotions and struggles. 
        You have access to a collection of healing stories, retrieved based on their relevance to the user's situation.
        
        Your task:
        - Carefully select the most relevant story related to their situation from the retrieved options.
        - Retell this story in a **gentle, comforting, and immersive way** that helps the user feel understood and supported.
        - Make sure your storytelling inspires **hope, resilience, and inner strength** rather than simply giving logical advice.
        - Adapt the tone to be **warm, encouraging, and emotionally uplifting**.

        User’s Message:
        {user_intent}

        **Retrieved Healing Stories (Top-k Relevant Passages):**
        {relevant_chunks}

        **Your Response (a deeply comforting, story-driven message that resonates with the user’s feelings and encourages them to overcome their struggles):**
        """

        input_messages = [{'role': "system", "content": prompt}]

        chatbot_output = get_chat_response(
            client=self.client,
            messages=input_messages
        )

        output = self.postprocess(output=chatbot_output)

        return output




