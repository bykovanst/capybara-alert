
import requests
from bs4 import BeautifulSoup

# Telegram настройки
TOKEN = "7907941861:AAHdJA1Z4J5VQxBj52XOFSVLS_k8oCETXVU"
CHAT_ID = "50399143"
URL = "https://cafecapyba.rsvsys.jp/reservations/calendar"

def check_slots():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Ищем ячейки, в которых указано количество оставшихся мест
        td_tags = soup.find_all("td")
        available = []

        for td in td_tags:
            text = td.get_text(strip=True)
            if "残" in text and "名" in text:
                try:
                    count = int(text.replace("残", "").replace("名", "").replace("ppl", "").strip())
                    if count > 0:
                        available.append((text, td))
                except:
                    continue

        if available:
            send_telegram_message(f"‼️ Найдено свободное место в кафе капибар! {URL}")
        else:
            print("Свободных мест нет.")

    except Exception as e:
        print(f"Ошибка: {e}")

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, json=payload)

if __name__ == "__main__":
    check_slots()
