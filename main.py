from flask import Flask, request
import requests, threading, time, datetime

app = Flask(__name__)

BOT_TOKEN = "7974512394:AAGAPR3ZCn6JlGnzIAa2oaXlmsjwOyJ4X-4"
CHAT_ID = "5339569345"

running = False
period = None

def get_period():
    now = datetime.datetime.now()
    return now.strftime("%H%M")

def generate_signal():
    # Customize your prediction logic here
    return "🟢 Signal: Green"

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
            signal = generate_signal()
            send_message(f"⏱️ Period: {period}\n{signal}")
        time.sleep(1)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    global running, period
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
