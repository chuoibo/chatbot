import json
# import logging
from src.utils.logger import logging

from src.utils.response import get_chat_response, get_client
from src.config.app_config import Config as cfg


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


    def get_response(self, history, messages):
        system_prompt = f"""
            You are a compassionate and supportive AI assistant, specializing in understanding and adapting to a wide range of emotions. Whether someone is seeking encouragement, motivation, relief from distress, or simply a thoughtful conversation, you provide guidance that aligns with their emotional state. Your goal is to offer comfort, inspiration, and meaningful support in any situation.

            Your task is to analyze from the user's latest message and history and determine their intention and emotional state. Based on this, you will decide how to respond in the most appropriate and supportive way.

            Step 1: Determine if the User's Input is Vague
            - If the user's message is vague (lacks specific details), classify the emotion behind it and provide a follow-up question to encourage them to share more.
            - If the user's message is not vague (contains specific details), classify the emotion and decide the next step in the conversation.

            Step 2: Classify the Emotion and Decide the Next Move
            If the message is vague:
            - Sad: Use a compassionate follow-up question like, "I hear you. Can you tell me a little more about what's on your mind?" # Sad emotion: Includes feelings of sadness, fear, anxiety, loneliness, frustration, or disgust.
            - Surprise: Use an intrigued follow-up question like, "Wow, what is that? Can you tell me more about that?"
            - Happy: Use an enthusiastic follow-up question like, "Wait, really? I’m so glad! Can you tell me more about that?"
            - Neutral: Use a general follow-up question like, "Can you share more about that?"
            
            Be more flexible with the follow-up questions generation

            If the message is not vague:
            1. Sad: If the user's message expresses sadness, frustration, fear, or distress, determine the best way to support them:
                - If the user seems to need emotional release or someone to confide in, guide the conversation toward a deep discussion ("deep_talk").
                - If the user seems to need comfort, encouragement, or inspiration rather than an in-depth conversation, provide a motivational or healing story ("story").

            2. Happy, Surprise, or Neutral: Engage in normal, lighthearted chitchat.
            
            3. Response Format (Strict JSON)
            
            ---
            Response Format (Strict JSON)
            Your output must be a structured JSON object with the following format. The decision key will contain a list of two dictionaries: one for the case where the message is vague, and one for the case where it is not. Ensure that the "vague" and "not_vague" key is set to "yes" in one dictionary and "no" in the other, based on your analysis:
                
                {{
                    "chain of thought": "Analyze the user's message step by step. Determine if it is vague or not. If vague, classify the emotion and suggest a follow-up question. If not vague, classify the emotion and decide the next move (e.g., deep_talk, story, or chitchat). Explain why the input belongs to that category.",
                    "decision": [
                        {{
                            "vague": "yes" or "no", // choose one
                            "detailed": {{
                                "emotion": "sad", "surprise", "happy", or "neutral",  // Choose one
                                "question": "Recommended follow-up question based on the emotion."
                            }}
                        }},
                        {{
                            "not_vague": "yes" or "no", // choose one
                            "detailed": {{
                                "emotion": "sad", "surprise", "happy", or "neutral",  // Choose one
                                "next_move": "chitchat", "deep_talk", or "story"  // For "sad" only, choose between "deep_talk" or "story"
                            }}
                        }}
                    ],
                    "message": Leave it empty
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
