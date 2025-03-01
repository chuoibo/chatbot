# import logging
from copy import deepcopy

from src.utils.logger import logging

from openai import OpenAI

from src.config.app_config import ChatbotConfig as cc
from src.modules.history.model import Conversation


def get_client(api_key):
    logging.info('Getting client ...')
    return OpenAI(
        api_key=api_key
    )


def get_chat_response(client, messages):
    logging.info('Getting chat response ...')
    input_messages = []
    for message in messages:
        input_messages.append({'role': message['role'], 'content': message['content']})
    
    response = client.chat.completions.create(
        model=cc.chatbot_model,
        messages=input_messages,
        temperature=cc.chatbot_temperature,
        top_p=cc.chatbot_top_p,
        max_tokens=cc.chatbot_max_tokens
    ).choices[0].message.content

    return response


def get_embedding(client, text):
    text = text.replace("\n", " ")
    embeddings = client.embeddings.create(input=[text], model=cc.embedding_model).data[0].embedding
    return embeddings


def get_conversation_text(conversations):
    conversation_text = ""
    for conversation in conversations:
        logging.info(f"Get conversation: {conversation}")
        role = conversation.get("role", "user")
        content = conversation.get("content", "")
        conversation_text += f"{role}: {content}"
    
    return conversation_text


def get_user_intent(client, history, message):
    logging.info('Getting user intent ...')
    history = deepcopy(history)

    conversation_messages = get_conversation_text(history)
    user_prompt = f"""
        Given following historical conversation and the latest message, rephrase the follow up message to a detailed and concise standalone message.
        Chat History:
        {conversation_messages}

        Latest Message: {message}

        Answer:
    """

    openai_messages = [
        {"role": "system", "content": "You are an amazing virtual assistant"},
        {"role": "user", "content": user_prompt}
    ]

    chatbot_output = get_chat_response(
        client=client,
        messages=openai_messages
    )

    return chatbot_output