import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

def get_model(**kwargs):
    return ChatOpenAI(temperature=0, **kwargs)

def create_basic_chain(chat_model, chat_prompt_template):
    chain = chat_prompt_template | chat_model
    return chain 

def main():    
    prompt = ChatPromptTemplate.from_template('Tell me the most noteworthy books by the author {author}')
    chat_model = get_model()
    
    chain = create_basic_chain(chat_model=chat_model, chat_prompt_template=prompt) | StrOutputParser()
    
    results = chain.invoke({'author': 'William Faulkner'})
    print(results)
    
if __name__ == '__main__':
    main()
