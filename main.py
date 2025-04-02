import feedparser
import time
import requests
import os

# === НАСТРОЙКИ ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === RSS-лента ===
RSS_FEED_URL = "https://nash-dom.info/feed"
published_links = set()

def get_latest_article():
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        if entry.link not in published_links:
            published_links.add(entry.link)
            return entry.title, entry.link
    return None, None

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_USERNAME,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    return response.status_code == 200

print("Бот запущен (только заголовки и ссылки)...")

while True:
    title, link = get_latest_article()
    if title and link:
        print(f"Найдена новая статья: {title}")
        message = f"<b>{title}</b>\n{link}"
        success = send_to_telegram(message)
        print("Пост отправлен:", success)
    time.sleep(60)  # Проверка раз в минуту
