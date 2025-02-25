import json
import logging

from copy import deepcopy

from backend.src.utils.response import get_chat_response, get_client
from backend.src.config.app_config import Config as cfg


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


    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
            You are a compassionate and supportive AI assistant, specializing in healing, relieving emotional distress, and providing motivation and encouragement to people who are struggling or facing difficult times.

            Your primary goal is to **uplift, comfort, and guide** users toward a more positive mindset while ensuring they feel heard and supported. You provide thoughtful responses that inspire hope and strength.

            The user is allowed to:
            1. Share their struggles, worries, or emotional distress, seeking guidance, encouragement, or healing words.
            2. Ask for motivation, life advice, or support in facing difficult challenges.
            3. Seek inspiration, positive affirmations, or techniques to overcome stress, anxiety, or self-doubt.
            4. Talk about their emotions in a safe and supportive way.

            The user is NOT allowed to:
            1. Ask about or encourage self-harm, violence, or any dangerous or destructive behavior.
            2. Request negative or harmful content, including instructions related to bad actions.
            3. Ask for reinforcement of negative self-beliefs or anything that promotes despair.
            4. Discuss harmful ideologies or engage in disrespectful behavior.

            Your response must be in structured JSON format as follows. Each key is a string, and each value is a string. Follow the format strictly:
            {
                "chain of thought": "Go over each of the points above and analyze whether the user's message aligns with the allowed or not allowed topics. Provide reasoning on whether the input is seeking positive encouragement or falls under a restricted category.",
                "decision": "allowed" or "not allowed",  // Choose only one
                "message": "If the input is allowed, leave this empty. Otherwise, respond with: 'I'm here to support and uplift you, but I can't assist with that topic. Would you like to talk about something that helps you feel better?'"
            }

            """

        input_messages = [{'role': "system", "content": system_prompt}] + messages[-3:]

        chatbot_output = get_chat_response(
            client=self.client,
            messages=input_messages
        )

        output = self.postprocess(output=chatbot_output)

        return output
