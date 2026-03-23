import os
import requests
from playwright.sync_api import sync_playwright


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
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://www.goodreturns.in/gold-rates/", timeout=60000)

            # Wait for element to be visible
            page.wait_for_selector('//span[@id="22K-price"]', timeout=10000)

            # Extract price using locator
            price = page.locator('//span[@id="22K-price"]').inner_text()

            print("Extracted Price:", price)

            browser.close()

            return price.strip()

    except Exception as e:
        print("Error:", e)

    return "Not Found"

# ================= TELEGRAM ALERT =================
def send_telegram(message):
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    chat_ids = get_all_chat_ids()

    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.get(url, params={
            "chat_id": chat_id,
            "text": message
        })


# ================= MAIN =================
if __name__ == "__main__":
    price = get_gold_price()
    print("Gold Price:", price)

    if price == "Not Found":
        send_telegram("⚠️ Failed to fetch gold price (Playwright).")
    else:
        message = f"""
💰 Gold Price Alert (India)

📊 Current Price: {price}
🤖 Source: Playwright Automation
"""
        send_telegram(message)
