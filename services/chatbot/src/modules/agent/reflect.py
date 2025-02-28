import json
# import logging
from src.utils.logger import logging

from src.utils.response import get_chat_response, get_client
from src.config.app_config import Config as cfg


class ReflectAgent:
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
                "agent": "reflect_agent",
                "reflect_agent": output['decision']
            }
        }

        return dict_output


    def get_response(self, history, messages):
        system_prompt = f"""
            You are a compassionate and supportive AI assistant, specializing in understanding and adapting to a wide range of emotions. Whether someone is seeking encouragement, motivation, relief from distress, or simply a thoughtful conversation, you provide guidance that aligns with their emotional state. Your goal is to offer comfort, inspiration, and meaningful support in any situation.

            Given the following chat history and the user's latest message, your task is to classify the **intention** of the user based on their input so that we can respond in the most appropriate manner.

            Determines if the user's input is too vague and whether a follow-up question is needed. If it is detailed enough

            Type of respond:
            1. "sad" : Includes feelings of sadness, fear, anxiety, loneliness, frustration, or disgust.
            - Example: "I feel so alone these days."
            - Example: "I'm scared about my future."
            - Example: "I don’t think I’m good enough."

            2. "happy": Includes feelings of joy, excitement, gratitude, love, and enthusiasm.
            - Example: "I'm so happy today!"
            - Example: "I just got a new job, and I'm really excited!"
            - Example: "I feel so grateful for my friends and family."

            3. "surprise": Includes feelings of astonishment, amazement, disbelief, and unexpected joy.
            - Example: "I can't believe this just happened!"
            - Example: "Wow! I never expected to win the contest!"
            - Example: "This is the best surprise ever!"

            4. "neutral": Includes factual, unemotional, or everyday conversations that don’t express strong emotions.
            - Example: "What do you think about meditation?"
            - Example: "I want to learn how to stay motivated."
            - Example: "Tell me some popular quotes."

            ---

            Response Format (Strict JSON)
            Your output must be a structured JSON object with the following format:

            {{
                "chain of thought": "Go over each of the points above and analyze whether the user's message conveys sadness, happiness, or a neutral tone. Explain why the input belongs to that category.",
                "decision": "sad" or "happy" or "surprise" or "neutral",  // Pick only one
                "message": ""  // Leave empty
            }}

            Chat History: {history}

            Latest User Message: {messages}
        """


        input_messages = [{'role': "system", "content": system_prompt}]

        chatbot_output = get_chat_response(
            client=self.client,
            messages=input_messages
        )

        output = self.postprocess(output=chatbot_output)

        return output
