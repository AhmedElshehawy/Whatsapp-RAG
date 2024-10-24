import os
import logging
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from local_loader import load_files_text
from splitter import split_documents
from time import sleep
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

class EmbeddingProxy:
    def __init__(self, embedding) -> None:
        self.embedding = embedding
        self.embed_delay = os.environ.get('EMBED_DELAY')
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        sleep(self.embed_delay)
        return self.embedding.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        sleep(self.embed_delay)
        return self.embedding.embed_query(text)


def create_vector_db(texts, embedding=None, collection_name='chroma')    :
    if not texts:
        logging.warning('Empty texts passed in to create vector database')
    
    if not embedding:
        embedding = OpenAIEmbeddings(model=os.environ.get('OPENAI_EMBED_MODEL'))
    
    proxy_embedding = EmbeddingProxy(embedding)
    
    db = Chroma(collection_name=collection_name, embedding_function=proxy_embedding, persist_directory=os.path.join('store/', collection_name))
    db.add_documents(texts)
    return db
    