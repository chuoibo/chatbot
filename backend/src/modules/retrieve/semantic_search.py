import logging

from pinecone import Pinecone

from backend.src.utils.response import get_client, get_embedding
from backend.src.config.app_config import (ChatbotConfig as cc,
                                           Config as cfg)


class SemanticSearch:
    def __init__(self):
        self.client = get_client(
            api_key=cfg.OPENAI_API_KEY
        )

        self.vector_database = Pinecone(api_key=cfg.VECTOR_DATABASE_API_KEY)
        self.vector_database_index_name = cc.vector_database_index_name
        self.vector_database_name_space = cc.vector_database_name_space

        logging.info('Initialize Semantic Search ...')

    
    def get_results(self):
        pass
