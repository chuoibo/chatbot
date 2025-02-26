# import logging
from src.utils.logger import logging


from pinecone import Pinecone

from llama_index.core import Document

from src.modules.retrieve.rerank import Reranker
from src.utils.response import get_client, get_embedding
from src.config.app_config import (ChatbotConfig as cc,
                                           Config as cfg)


class SemanticSearch:
    def __init__(self):
        self.client = get_client(
            api_key=cfg.OPENAI_API_KEY
        )

        self.vector_database = Pinecone(api_key=cfg.VECTOR_DATABASE_API_KEY)

        self.pinecone_index = self.vector_database.Index(cc.vector_database_index_name)

        self.rerank = Reranker()

        logging.info('Initialize Semantic Search ...')

    
    def retrieve_relevant_chunks(self, query):
        query_embedding = get_embedding(
            client=self.client,
            query=query
        )

        results = self.pinecone_index.query(
            namespace=cc.vector_database_name_space,
            vector=query_embedding,
            top_k=cc.retrieval_top_k,
            include_values=False,
            include_metadata=True
        )

        retrieved_docs = []
        for match in results['matches']:
            retrieved_docs.append(match['metadata']['text'])
        
        if not retrieved_docs:
            return []
        
        reranked_docs = self.rerank(query, retrieved_docs)
        final_docs = [Document(text=doc) for doc in reranked_docs]

        logging.info(f'Finish retrieveing relevant documents {final_docs} ...')
        
        return retrieved_docs