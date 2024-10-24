import os
import logging
from dotenv import load_dotenv, find_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from fastapi.responses import PlainTextResponse
from langchain import hub
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory
from ensemble import ensembel_retriever_from_docs
from rag_chain import make_rag_cahin, get_question
from local_loader import load_files_text
from basic_chain import create_basic_chain, get_model
from splitter import split_documents
from vector_store import create_vector_db
from memory import create_memory_chain


_ = load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_retriever():
    docs = load_files_text(file_extension='.pdf', data_dir='./data')
    embedding = OpenAIEmbeddings(model=os.environ.get('OPENAI_EMBED_MODEL'))
    return ensembel_retriever_from_docs(docs, embedding=embedding)

def get_chain():
    model = get_model(model=os.environ.get('OPENAI_CHAT_MODEL'))
    chat_memory = ChatMessageHistory()
    ensemble_retriever = get_retriever()
    output_parser = StrOutputParser()
    rag_chain = make_rag_cahin(model=model, retriever=ensemble_retriever)
    chain = create_memory_chain(model, rag_chain, chat_memory) | output_parser
    return chain

def run_rag_query(query):
    memory_chain = get_chain()
    response = memory_chain.invoke(
        {'question': query},
        config={'configurable': {'session_id': 'foo'}}
    )
    return response
