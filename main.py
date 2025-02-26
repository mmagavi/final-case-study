from typing import Union
from fastapi import FastAPI, Request
from agents.functionCallAgent import make_chat_request
import requests
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_KEY")
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

@app.get("/")

def read_root():

    return {"Hello": "World"}


@app.get("/chat/{user_input}")

def read_item(user_input: str):

    response = make_chat_request(user_input)[0]
    image_url = make_chat_request(user_input)[1]

    return {"user_input": user_input, "response": response, "image_url": image_url}



@app.post("/webhook")
async def handle_webhook(request: Request):
    # Get the incoming message from Telegram
    data = await request.json()

    # Extract relevant information (e.g., chat_id and message)
    chat_id = data['message']['chat']['id']
    user_message = data['message']['text']

    # Process the message (using your existing function or logic)
    response, image_url = make_chat_request(user_message)

    # Send a response back to the user
    if not image_url:
        response_text = f"{response}"
    else:
        response_text = f"{response}\n{image_url}"

    # Send the response via Telegram API
    response = requests.post(TELEGRAM_URL, json={
        'chat_id': chat_id,
        'text': response_text
    })

    return {"status": "ok"}


# Optional: To set the webhook, call this endpoint once to configure the webhook URL
@app.get("/set_webhook")
def set_webhook():
    ngrok_url = 'https://0125-69-193-135-214.ngrok-free.app/webhook'  # Replace with your ngrok or server URL
    webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={ngrok_url}"

    response = requests.get(webhook_url)
    
    if response.json().get('ok'):
        return {"status": "Webhook set successfully"}
    else:
        return {"status": "Failed to set webhook", "error": response.json()}