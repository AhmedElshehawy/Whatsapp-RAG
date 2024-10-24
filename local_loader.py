import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

DATA_LOADERS = {'.pdf': PyPDFLoader, '.txt': TextLoader, '.csv': CSVLoader}

def correct_file_extension(file_extension):
    file_extension = file_extension if file_extension.startswith('.') else f'.{file_extension}'
    return file_extension
def list_files(file_extension, data_dir='./data'):
    file_extension = correct_file_extension(file_extension)
    paths = Path(data_dir).glob(f'*{file_extension}')
    for path in paths:
        yield str(path)
        
def load_files(file_extension, data_dir='./data'):
    file_extension = correct_file_extension(file_extension)
    docs = []
    for path in list_files(file_extension=file_extension, data_dir=data_dir):
        print(f'Loading {path}')
        loader = DATA_LOADERS[file_extension]
        docs.extend(loader.load())
    return docs
    