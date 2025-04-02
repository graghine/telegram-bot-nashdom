import os
import requests
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{TELEGRAM_TOKEN}"

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот работает!'

@app.route(f'/webhook/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        text = data['message'].get('text', '')
        chat_id = data['message']['chat']['id']
        if text.lower() == 'ping':
            send_message(chat_id, "pong")
    return '', 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})
    print("Webhook set:", response.text)

if __name__ == '__main__':
    set_webhook()
