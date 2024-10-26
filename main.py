import os
import logging
from fastapi import FastAPI, Form, Depends, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from fastapi.responses import PlainTextResponse
from utils import logger, run_rag_query
from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

twilio_client = Client()
app = FastAPI()

def send_message(to_number, body_text):
    try:
        message = twilio_client.messages.create(
            from_=f"whatsapp:{os.environ.get('TWILIO_NUMBER')}",
            body=body_text,
            to=f"whatsapp:{to_number}"
            )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")
@app.post('/message')
async def reply(request: Request, Body: str=Form()):#, db: Session=Depends(get_db)):
    logger.info('Sending WhatsApp Message')
    
    form_data = await request.form()
    whatsapp_number = form_data['From'].split('whatsapp:')[-1]
    print(f'Sending the LangChain response to this number: {whatsapp_number}')
    
    langchain_response = run_rag_query(Body)
        
    # Now send the message
    send_message(whatsapp_number, langchain_response)
    return ''
        