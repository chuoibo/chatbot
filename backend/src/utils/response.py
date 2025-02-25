import logging

from openai import OpenAI

from backend.src.config.app_config import ChatbotConfig as cc


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