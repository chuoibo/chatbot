# import logging
from src.utils.logger import logging


from redis import Redis
from src.utils.common import generate_request_id
from src.config.app_config import (ChatbotConfig as cbc,
                                           Config as cfg)


class Cache:
    def __init__(self, bot_id, user_id):
        self.bot_id = bot_id
        self.user_id = user_id
        self.redis_client = Redis.from_url(url='redis://:PASSWORD@localhost:6379/0')

    def get_conversation_key(self):
        return f"{self.bot_id}.{self.user_id}"


    def get_conversation_id(self):
        key = self.get_conversation_key()
        try:
            if self.redis_client.exists(key):
                logging.info('This key for this conversation has already existed !')
                self.redis_client.expire(key, cbc.ttl_seconds)
                return self.redis_client.get(key).decode('utf-8')
            else:
                logging.info('Generate new key for this conversation !')
                conversation_id = generate_request_id(length=cbc.length_string,
                                                      max_length=cbc.max_length_string)
                return conversation_id

        except Exception as e:
            logging.exception(f'Get conversation error {e}')
            return None
        
    
    def clear_conversation(self):
        key = self.get_conversation_id()
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logging.exception(f'Delete conversation error {e}')
            return False
            
            