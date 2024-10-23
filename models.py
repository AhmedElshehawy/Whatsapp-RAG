import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

url = URL.create(
    drivername='postgresql',
    username=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host='localhost',
    database=os.environ.get('DATABASE'),
    port=os.environ.get('PORT')
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversaions'
    
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    message = Column(String)
    response = Column(String)

Base.metadata.create_all(engine)
