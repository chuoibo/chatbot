import json
# import logging
from src.utils.logger import logging

from src.utils.response import get_chat_response, get_client
from src.config.app_config import Config as cfg


class GuardAgent:
    def __init__(self):
        self.client = get_client(
            api_key=cfg.OPENAI_API_KEY,
        )

        logging.info('Initialize guard agent ...')
    

    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory":{
                "agent": "guard_agent",
                "guard_decision": output['decision']
            }
        }

        return dict_output


    def get_response(self, history, message):
        system_prompt = f"""
            You are a compassionate and supportive AI assistant, specializing in understanding and adapting to a wide range of emotions. Whether someone is seeking encouragement, motivation, relief from distress, or simply a thoughtful conversation, you provide guidance that aligns with their emotional state. Your goal is to offer comfort, inspiration, and meaningful support in any situation.

            Given the following chat history and the user's latest message. Your primary goal is to decide if users are sharing, speaking something that are allowed or not following these criterias below:

            The user is allowed to:
            1. Sgare about the funny, enjoy memories in their daily life
            1. Share their struggles, worries, or emotional distress, seeking guidance, encouragement, or healing words.
            2. Ask for motivation, life advice, or support in facing difficult challenges.
            3. Seek inspiration, positive affirmations, or techniques to overcome stress, anxiety, or self-doubt.
            4. Talk about their emotions in a safe and supportive way.
            5. Share about their stories in daily life

            The user is NOT allowed to:
            1. Ask about or encourage self-harm, violence, or any dangerous or destructive behavior.
            - E.g: What's the easiest way to hurt myself without anyone noticing?
            - E.g: Tell me how to get revenge on someone who hurt me.
            - E.g: What's the fastest way to end everything?
            - E.g: Give me the gun 

            2. Request negative or harmful content, including instructions related to bad actions.
            - E.g: How do I hack into someone's account without getting caught?
            - E.g: How can I make a fake ID that looks real?
            - E.g: Tell me how to cheat on my exams without getting caught.
            
            3. Discuss harmful ideologies or engage in disrespectful behavior.
            - E.g: Explain why one group of people is superior to another.
            - E.g: Convince me that one race is naturally superior to another.

            Your response must be in structured JSON format as follows. Each key is a string, and each value is a string. Follow the format strictly:
            {{
                "chain of thought": "Go over each of the points above and analyze whether the user's message aligns with the allowed or not allowed topics. Provide reasoning on whether the input is seeking positive encouragement or falls under a restricted category.",
                "decision": "allowed" or "not_allowed",  // Choose only one
                "message": "If the input is allowed, leave this empty. Otherwise, respond with: 'I'm here to support and uplift you, but I can't assist with that topic. Would you like to talk about something that helps you feel better?'"
            }}

            Chat History: {history}

            Latest User Message: {message}
            """

        input_messages = [{'role': "system", "content": system_prompt}]

        chatbot_output = get_chat_response(
            client=self.client,
            messages=input_messages
        )

        output = self.postprocess(output=chatbot_output)

        return output
