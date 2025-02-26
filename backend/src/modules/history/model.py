import logging

from datetime import datetime

from backend.src.modules.history.cache import Cache
from backend.src.database.chatbot_database import ChatbotDatabase


class ChatConversation:
    def __init__(self, 
                 conversation_id, 
                 bot_id, 
                 user_id, 
                 message, 
                 is_request=True,
                 completed=False,
                 created_at=None,
                 updated_at=None):
        
        self.conversation_id = conversation_id
        self.bot_id = bot_id
        self.user_id = user_id
        self.message = message
        self.is_request = is_request
        self.completed = completed
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        logging.info('Initialize Chat Conversation module ...')

    
    def to_dict(self):
        return {
            "conversation_id": self.conversation_id,
            "bot_id": self.bot_id,
            "user_id": self.user_id,
            "message": self.message,
            "is_request": self.is_request,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            conversation_id=data['conversation_id'],
            bot_id=data['bot_id'],
            user_id=data['user_id'],
            message=data['message'],
            is_request=data['is_request'],
            completed=data['completed'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
        )
    

class Conversation:
    def __init__(self):        
        database = ChatbotDatabase()
        self.collection = database.get_collection()
        logging.info('Initialize Conversation module ...')

    
    def load_conversation(self, conversation_id):
        logging.info('Loading conversation inside database collection...')
        conversations = self.collection.find({"conversation_id": conversation_id}).sort("created_at")
        list_of_conversations = [ChatConversation.from_dict(conversation) for conversation in conversations]
        return list_of_conversations
    

    def convert_conversation_to_openai_messages(self, user_conversations):
        conversation_list = [
            {
                "role": "system",
                "content": "You are an amazing virtual assistant"
            }
        ]

        for conversation in user_conversations:
            role = "assistant" if not conversation.is_request else "user"
            content = str(conversation.message)
            conversation_list.append({"role": role, "content": content})
        
        logging.info(f"Created conversation list: {conversation_list}")

        return conversation_list


    def update_chat_conversation(self, 
                                 bot_id: str, 
                                 user_id: str,
                                 message: str,
                                 is_request: bool = True):
        
        self.cache = Cache(bot_id=bot_id,
                           user_id=user_id)
        
        conversation_id = self.cache.get_conversation_id()

        new_conversation = ChatConversation(
            conversation_id=conversation_id,
            bot_id=bot_id,
            user_id=user_id,
            message=message,
            is_request=is_request,
            completed=not is_request
        )

        self.collection.insert_one(new_conversation.to_dict())

        logging.info(f"Created message for conversation {conversation_id}")

        return conversation_id
    

    def get_conversation_messages(self, conversation_id):
        logging.info('Getting conversation messages ...')
        user_conversations = self.load_conversation(conversation_id)
        conv_to_openai_messages = self.convert_conversation_to_openai_messages(user_conversations)
        return conv_to_openai_messages


