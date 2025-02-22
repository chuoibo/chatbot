import os
import logging
from dotenv import load_dotenv

from backend.src.utils.common import read_yaml_file
from backend.src.config import CHATBOT_CONFIG_FILE, DATABASE_CONFIG_FILE

load_dotenv()


class Config:
    RMQ_USER = os.getenv('RMQ_USER', 'guest')
    RMQ_PWD = os.getenv('RMQ_PWD', 'guest')
    MQ_URL = os.getenv('MQ_URL', f'amqp://{RMQ_USER}:{RMQ_PWD}@rabbitmq:5672/')
    
    REDIS_PWD = os.getenv('REDIS_PWD', '')
    REDIS_URL = os.getenv('REDIS_URL', f'redis://:{REDIS_PWD}@redis:6379/0')

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    VECTOR_DATABASE_API_KEY = os.getenv("PINECONE_API_KEY")

    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


class ChatbotConfig:
    chatbot_file = read_yaml_file(CHATBOT_CONFIG_FILE)
    chatbot = chatbot_file['chatbot']
    cache = chatbot_file['cache']

    chatbot_model = chatbot['model']
    chatbot_temperature = chatbot['temperature']
    chatbot_top_p = chatbot['top_p']
    chatbot_max_tokens = chatbot['max_tokens']

    ttl_seconds = cache['ttl_seconds']
    length_string = cache['length_string']
    max_length_string = cache['max_length_string']


class DatabaseConfig:
    def __init__(self):
        self.config = read_yaml_file(DATABASE_CONFIG_FILE)
        logging.info('Init Chatbot Database configuration parameters')

    def init_database(self):
        return self.config['database']
