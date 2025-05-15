
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Настройки из GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")  # Несколько получателей через запятую

URL = "https://cafecapyba.rsvsys.jp/reservations/calendar"

def check_slots():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        td_tags = soup.find_all("td")
        available = []

        for td in td_tags:
            text = td.get_text(strip=True)
            if "残" in text and "名" in text:
                try:
                    count = int(text.replace("残", "").replace("名", "").replace("ppl", "").strip())
                    if count > 0:
                        available.append(text)
                except:
                    continue

        now = datetime.now().strftime('%Y-%m-%d %H:%M')

        if available:
            message = f"‼️ <b>{now}: Найдено место в кафе капибар!</b>\n\n<a href=\"{URL}\">🔗 Перейти к бронированию</a>"
        else:
            message = f"⏱ {now}: Проверка выполнена — мест нет."

        send_telegram_message(message, available != [])

    except Exception as e:
        send_telegram_message(f"❗ Ошибка при проверке: {e}", is_html=False)

def send_telegram_message(message, is_html=True):
    for chat_id in CHAT_IDS:
        payload = {
            "chat_id": chat_id.strip(),
            "text": message,
            "parse_mode": "HTML" if is_html else "Markdown",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": "🔗 Забронировать", "url": URL}]
                ]
            } if is_html else None
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json=payload)

if __name__ == "__main__":
    check_slots()
