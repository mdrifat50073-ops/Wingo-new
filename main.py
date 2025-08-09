from flask import Flask, request
import time, threading, requests

app = Flask(__name__)

# 🔐 Bot credentials
BOT_TOKEN = "7974512394:AAGAPR3ZCn6JlGnzIAa2oaXlmsjwOyJ4X-4"
CHAT_ID = "6848807471"

# 🔄 Loop control
running = False

def send_prediction():
    message = "📡 Wingo Signal: Red ✅"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def loop():
    global running
    while running:
        send_prediction()
        time.sleep(60)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    global running
    data = request.get_json()
    if "message" in data:
        text = data["message"].get("text", "")
        chat_id = data["message"]["chat"]["id"]

        if text == "/start":
            if not running:
                running = True
                threading.Thread(target=loop).start()
                reply = "✅ Bot Started"
            else:
                reply = "⚠️ Bot already running"

        elif text == "/stop":
            if running:
                running = False
                reply = "🛑 Bot Stopped"
            else:
                reply = "⚠️ Bot is not running"

        else:
            reply = "🤖 Unknown command"

        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      data={"chat_id": chat_id, "text": reply})

    return "ok"

# 🚀 Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
