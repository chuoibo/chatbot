import os
from dotenv import load_dotenv

from backend.src.utils.common import read_yaml_file
from backend.src.config import CHATBOT_CONFIG_FILE

load_dotenv()


class Config:
    RMQ_USER = os.getenv('RMQ_USER', 'guest')
    RMQ_PWD = os.getenv('RMQ_PWD', 'guest')
    MQ_URL = os.getenv('MQ_URL', f'amqp://{RMQ_USER}:{RMQ_PWD}@rabbitmq:5672/')
    
    # Redis Configuration
    REDIS_PWD = os.getenv('REDIS_PWD', '')
    REDIS_URL = os.getenv('REDIS_URL', f'redis://:{REDIS_PWD}@redis:6379/0')

    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    VECTOR_DATABASE_API_KEY = os.getenv("PINECONE_API_KEY")


class ChatbotConfig:
    chatbot_file = read_yaml_file(CHATBOT_CONFIG_FILE)
    chatbot = chatbot_file['chatbot']

    chatbot_model = chatbot['model']
    chatbot_temperature = chatbot['temperature']
    chatbot_top_p = chatbot['top_p']
    chatbot_max_tokens = chatbot['max_tokens']
