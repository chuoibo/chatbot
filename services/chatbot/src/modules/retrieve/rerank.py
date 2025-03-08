# import logging
from src.utils.logger import logging

from typing import List
from FlagEmbedding import FlagReranker

from src.config.app_config import ChatbotConfig as cc


class Reranker:
    def __init__(self):
        self.reranker = FlagReranker(model_name_or_path=cc.rerank_model,
                                     use_fp16=cc.use_fp16)
                
        logging.info('Initialize the BGE reranker ...')

    
    def calculate_scores(self, pairs: List[List[str]]) -> List[float]:
        logging.info('Calculate score for pair of document and query ...')
        
        scores = self.reranker.compute_score(pairs, normalize=True)
        return scores
    

    def rerank(self, query: str, docs: List[str]) -> List[str]:
        logging.info('Rerank query and list of retrieved documents ...')
        
        pairs = [[query, doc] for doc in docs]
        list_scores = self.calculate_scores(pairs=pairs)
        doc_scores = list(zip(docs, list_scores))
        sorted_doc_scores = sorted(doc_scores, key=lambda x: x[1], reverse=True)
        top_k_documents = [doc for doc, _ in sorted_doc_scores[:cc.rerank_top_k]]
        
        logging.info(f'Finish rerank model with top_docs {top_k_documents}')
        return top_k_documents

