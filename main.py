import feedparser
import time
import requests
import os
from datetime import datetime, timedelta

# === Настройки ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
RSS_FEED_URL = "https://nash-dom.info/feed"

# === Загрузка уже отправленных ссылок ===
def load_sent_links():
    try:
        with open("sent.txt", "r") as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def save_sent_link(link):
    with open("sent.txt", "a") as f:
        f.write(link + "\n")

# === Проверка, что статья новая (опубликована за последние 24 часа) ===
def is_recent(entry, hours=24):
    if not hasattr(entry, 'published_parsed'):
        return False
    published = datetime.fromtimestamp(time.mktime(entry.published_parsed))
    return datetime.utcnow() - published <= timedelta(hours=hours)

# === Получение новой статьи ===
def get_latest_article(sent_links):
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        if entry.link not in sent_links and is_recent(entry):
            return entry
    return None

# === Отправка поста в Telegram ===
def send_to_telegram(title, link):
    text = f"<b>{title}</b>\n{link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_USERNAME,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    return response.ok

# === Главный цикл ===
print("Бот запущен — фильтрует по дате (24ч) и не дублирует статьи.")

sent_links = load_sent_links()

while True:
    article = get_latest_article(sent_links)
    if article:
        print("Новая статья:", article.title)
        success = send_to_telegram(article.title, article.link)
        print("Отправка успешна:", success)
        sent_links.add(article.link)
        save_sent_link(article.link)
    time.sleep(300)  # Проверка каждые 5 минут
