import os
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.output_parsers import StrOutputParser
from basic_chain import get_model
from rag_chain import make_rag_cahin
from splitter import split_documents
from vector_store import create_vector_db
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def ensembel_retriever_from_docs(docs, embedding=None):
    texts = split_documents(docs)
    vs = create_vector_db(texts, embedding)
    vs_retriever = vs.as_retriever()
    
    bm25_retriever = BM25Retriever.from_texts([t.page_content for t in texts])
    
    bm25_weight = float(os.environ.get('BM25_RETRIEVER_WEIGHT'))
    vs_weight = 1.0 - bm25_weight
    ensembel_retriever = EnsembleRetriever(retrievers=[bm25_retriever, vs_retriever], weights=[bm25_weight, vs_weight])
    return ensembel_retriever
