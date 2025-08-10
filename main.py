import requests
import datetime
import time

BOT_TOKEN = "7974512394:AAGAPR3ZCn6JlGnzIAa2oaXlmsjwOyJ4X-4"
CHAT_ID = "6848807471"
is_running = False
last_update_id = None

def get_period():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M")

def predict(period):
    digit = int(str(period)[-1])
    size = "Big" if digit in [1, 4, 5, 7, 8] else "Small"
    color = "Red" if digit in [1, 4, 7] else "Green" if digit in [2, 5, 8] else "Violet"
    return size, color

def send_signal():
    period = get_period()
    size, color = predict(period)
    message = f"""🎲 Wingo 1-Minute Prediction

🕒 Period: {period}
📊 Result: {size}
🎨 Colour: {color}
✅ Signal sent automatically."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_command():
    global is_running, last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": last_update_id, "timeout": 5}
    response = requests.get(url, params=params).json()

    if "result" in response:
        for update in response["result"]:
            last_update_id = update["update_id"] + 1
            if "message" in update and "text" in update["message"]:
                text = update["message"]["text"]
                if text == "/start":
                    is_running = True
                    send_text("✅ Signal started.")
                elif text == "/stop":
                    is_running = False
                    send_text("🛑 Signal stopped.")

def send_text(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

# 🔁 Main loop
while True:
    check_command()
    if is_running:
        send_signal()
        time.sleep(60)
    else:
        time.sleep(3)
