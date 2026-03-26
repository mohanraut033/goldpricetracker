import os
import requests
from playwright.sync_api import sync_playwright


# ================= GET ALL USERS =================
def get_all_chat_ids():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    response = requests.get(url).json()

    chat_ids = set()

    for item in response.get("result", []):
        if "message" in item:
            chat_ids.add(item["message"]["chat"]["id"])

    return list(chat_ids)


# ================= FETCH GOLD PRICE =================
def get_gold_price():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://www.goodreturns.in/gold-rates/", timeout=60000)

            page.wait_for_selector('xpath=//span[@id="22K-price"]', timeout=10000)
            price = page.locator('xpath=//span[@id="22K-price"]').inner_text()

            print("Extracted Price:", price)

            browser.close()

            return price.strip()

    except Exception as e:
        print("Error:", e)

    return "Not Found"


# ================= TELEGRAM ALERT =================
def send_telegram(message):
    print("Sending message to Telegram...")

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    chat_ids = get_all_chat_ids()   # ✅ FIXED HERE

    print("Chat IDs found:", chat_ids)

    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        response = requests.get(url, params={
            "chat_id": chat_id,
            "text": message
        })

        print(f"Response for {chat_id}:", response.text)


# ================= MAIN =================
if __name__ == "__main__":
    price = get_gold_price()
    print("Gold Price:", price)

    message = ""

    if price == "Not Found":
        message = "⚠️ Failed to fetch gold price (Playwright)."
    else:
        message = f"""
💰 Gold Price Alert (India)

📊 Current Price: {price}
🤖 Source: Playwright Automation
"""

    print("About to send message...")
    send_telegram(message)
