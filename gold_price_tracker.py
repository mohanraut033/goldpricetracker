import requests
from bs4 import BeautifulSoup
import os


# ================= FETCH GOLD PRICE =================
def get_gold_price():
    import requests
    from bs4 import BeautifulSoup

    try:
        url = "https://www.bankbazaar.com/gold-rate.html"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find table values
        rows = soup.find_all("td")

        for row in rows:
            text = row.get_text(strip=True)
            if "₹" in text and len(text) < 15:
                return text

    except Exception as e:
        print("Error:", e)

    return "Not Found"

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
