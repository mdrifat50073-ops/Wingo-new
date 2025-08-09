from flask import Flask, request
import requests, threading, time, datetime

app = Flask(__name__)

BOT_TOKEN = "7974512394:AAGAPR3ZCn6JlGnzIAa2oaXlmsjwOyJ4X-4"
CHAT_ID = "6848807471"

running = False
period = None

def get_period():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")  # Unique period format

def predict(period):
    digit = int(str(period)[-1])
    size = "Big" if digit in [1, 4, 5, 7, 8] else "Small"
    color = "Red" if digit in [1, 4, 7] else "Green" if digit in [2, 5, 8] else "Violet"
    return size, color

def generate_message(period):
    size, color = predict(period)
    return f"""🎲 Number Prediction for Hgnice-App

🎯 Period: {period}
🎰 Result: {size}
💠 Colour: {color}"""

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

def signal_loop():
    global running, period
    while running:
        current = get_period()
        if current != period:
            period = current
            msg = generate_message(period)
            send_message(msg)
        time.sleep(1)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    global running
    data = request.get_json()

    if "message" in data:
        text = data["message"].get("text", "")
        chat_id = str(data["message"]["chat"]["id"])

        if chat_id != CHAT_ID:
            return "Unauthorized", 403

        if text == "/start":
            if not running:
                running = True
                threading.Thread(target=signal_loop).start()
                send_message("✅ Bot Started")
        elif text == "/stop":
            running = False
            send_message("🛑 Bot Stopped")
        else:
            send_message("🤖 Use /start or /stop")

    return "OK", 200

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
