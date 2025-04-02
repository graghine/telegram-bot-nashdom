import feedparser
import time
import requests
import os

TELEGRAM_TOKEN = os.getenv("7756641033:AAGXj2ywYtdnaZlgZFKBtF_Yj9ud0pimR0w
")
CHANNEL_USERNAME = os.getenv("@oh_new_by")

RSS_FEED_URL = "https://nash-dom.info/feed"
published_links = set()

def get_latest_article():
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        if entry.link not in published_links:
            published_links.add(entry.link)
            return {
                "title": entry.title,
                "link": entry.link
            }
    return None

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_USERNAME,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    return response.status_code == 200

print("Бот запущен (заголовки + ссылки)...")
while True:
    article = get_latest_article()
    if article:
        print("Новая статья:", article["title"])
        text = f"<b>{article['title']}</b>\n\nЧитать: {article['link']}"
        success = send_to_telegram(text)
        print("Успешно отправлено:", success)
    time.sleep(300)
