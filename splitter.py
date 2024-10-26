import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


CHUNK_SIZE = os.environ.get('CHUNK_SIZE')
CHUNK_OVERLAP = os.environ.get('CHUNK_OVERLAP')

def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(CHUNK_SIZE),
        chunk_overlap=int(CHUNK_OVERLAP),
        length_function=len,
        is_separator_regex=False
    )
    
    contents = docs
    if docs and isinstance(docs[0], Document)   :
        contents = [doc.page_content for doc in docs]
    
    texts = text_splitter.create_documents(contents)
    n_chunks = len(texts)
    print(f'Split into {n_chunks} chunks')
    return texts
    