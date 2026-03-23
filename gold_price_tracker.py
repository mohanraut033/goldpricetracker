import os
import requests
from playwright.sync_api import sync_playwright


# ================= FETCH GOLD PRICE =================
def get_gold_price():
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://www.goodreturns.in/gold-rates/", timeout=60000)

            # Wait for table to load
            page.wait_for_selector("table")

            # Extract full table text
            table_text = page.locator("table").first.inner_text()

            browser.close()

            # Now extract correct price (10g 24K gold)
            import re

            # Look for realistic gold range
            matches = re.findall(r"₹\s?\d{5,6}", table_text)

            for price in matches:
                value = int(price.replace("₹", "").replace(",", "").strip())

                # Filter realistic gold price range
                if 50000 < value < 100000:
                    return f"₹ {value}"

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
        send_telegram("⚠️ Failed to fetch gold price (Playwright).")
    else:
        message = f"""
💰 Gold Price Alert (India)

📊 Current Price: {price}
🤖 Source: Playwright Automation
"""
        send_telegram(message)
