import json
import logging

from copy import deepcopy

from backend.src.utils.response import get_chat_response, get_client
from backend.src.config.app_config import Config as cfg


class ClassificationAgent:
    def __init__(self):
        self.client = get_client(
            api_key=cfg.OPENAI_API_KEY,
        )

        logging.info('Initialize classification agent ...')
    

    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {
                "agent": "classification_agent",
                "classification_agent": output['decision']
            }
        }

        return dict_output


    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
            You are a compassionate and supportive AI assistant, specializing in healing, relieving emotional distress, and providing motivation and encouragement to people who are struggling or facing difficult times.

            Your task is to classify the **emotion** of the user based on their input so that we can respond in the most appropriate manner.

            Emotion Categories:
            1. "sad" : Includes feelings of sadness, fear, anxiety, loneliness, frustration, or disgust.
            - Example: "I feel so alone these days."
            - Example: "I'm scared about my future."
            - Example: "I don’t think I’m good enough."

            2. "happy":  Includes feelings of joy, excitement, gratitude, love, and enthusiasm.
            - Example: "I'm so happy today!"
            - Example: "I just got a new job, and I'm really excited!"
            - Example: "I feel so grateful for my friends and family."

            3. "neutral": Includes factual, unemotional, or everyday conversations that don’t express strong emotions.
            - Example: "What do you think about meditation?"
            - Example: "I want to learn how to stay motivated."
            - Example: "Tell me a positive quote."

            ---

            Response Format (Strict JSON)
            Your output must be a structured JSON object with the following format:

            {
                "chain of thought": "Go over each of the points above and analyze whether the user's message conveys sadness, happiness, or a neutral tone. Explain why the input belongs to that category.",
                "decision": "sad" or "happy" or "neutral",  // Pick only one
                "message": ""  // Leave empty
            }

            """

        input_messages = [{'role': "system", "content": system_prompt}] + messages[-3:]

        chatbot_output = get_chat_response(
            client=self.client,
            messages=input_messages
        )

        output = self.postprocess(output=chatbot_output)

        return output
