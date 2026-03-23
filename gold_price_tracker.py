import requests
from bs4 import BeautifulSoup
import os


# ================= FETCH GOLD PRICE =================
def get_gold_price():
    headers = {"User-Agent": "Mozilla/5.0"}

    urls = [
        "https://www.goodreturns.in/gold-rates/",
        "https://www.livechennai.com/gold_silverrate.asp"
    ]

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            selectors = [
                ("span", {"class": "gr-rt"}),
                ("td", {"class": "goldRate"})
            ]

            for tag, attrs in selectors:
                result = soup.find(tag, attrs)
                if result:
                    return result.text.strip()

        except Exception as e:
            print(f"Error with {url}: {e}")

    return "Not Found"


# ================= PRICE CHANGE CHECK =================
def has_price_changed(new_price):
    file_path = "last_price.txt"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            old_price = f.read().strip()
    else:
        old_price = ""

    if new_price != old_price:
        with open(file_path, "w") as f:
            f.write(new_price)
        return True

    return False


# ================= TELEGRAM ALERT =================
def send_telegram(message):
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.get(url, params={
        "chat_id": CHAT_ID,
        "text": message
    })


# ================= MAIN =================
if __name__ == "__main__":
    price = get_gold_price()
    print("Gold Price:", price)

    if price == "Not Found":
        send_telegram("⚠️ Failed to fetch gold price. Scraper issue.")
    else:
        if has_price_changed(price):
            message = f"""
💰 Gold Price Alert (India)

📊 Current Price: {price}
⏰ Auto-checked via GitHub Actions

#GoldTracker #Automation
"""
            send_telegram(message)
        else:
            print("No price change. No alert sent.")
