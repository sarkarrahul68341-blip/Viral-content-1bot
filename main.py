import os
import requests
from flask import Flask, request

TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

PHOTO_FILE = "welcome_photo.txt"

def get_saved_photo():
    if os.path.exists(PHOTO_FILE):
        with open(PHOTO_FILE, "r") as f:
            return f.read().strip()
    return None

def save_photo_id(file_id):
    with open(PHOTO_FILE, "w") as f:
        f.write(file_id)

app = Flask(__name__)

PACKAGES = {
    "pkg_1": {"name": "01 CP Video and File", "price": 249, "payment_link": "https://rzp.io/l/testlink", "content_link": "https://t.me/+iLoNw5R4Qwk5MGI1"},
    "pkg_2": {"name": "02 Rap & Big File", "price": 89, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_3": {"name": "03 Mom & Son", "price": 45, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_4": {"name": "04 Insta Viral", "price": 30, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_5": {"name": "05 Ganga Bath", "price": 199, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_6": {"name": "06 CP Bath Hidden", "price": 55, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_7": {"name": "07 Pakistani Girl", "price": 49, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_8": {"name": "08 Sister & Brother", "price": 30, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
}

def send_telegram_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return requests.post(url, json=payload).json()

def send_telegram_photo(chat_id, photo_id, caption, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": photo_id, "caption": caption, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return requests.post(url, json=payload).json()

def edit_message_text(chat_id, message_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return requests.post(url, json=payload).json()

def get_main_menu_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "🔑 01 CP Video - ₹249", "callback_data": "pkg_1"}],
            [{"text": "🔑 02 Rap & Big File - ₹89", "callback_data": "pkg_2"}],
            [{"text": "🔑 03 Mom & Son - ₹45", "callback_data": "pkg_3"}],
            [{"text": "🔞 04 Insta Viral - ₹30", "callback_data": "pkg_4"}],
            [{"text": "🔥 05 Ganga Bath - ₹199", "callback_data": "pkg_5"}],
            [{"text": "🔥 06 CP Bath Hidden - ₹55", "callback_data": "pkg_6"}],
            [{"text": "🔥 07 Pakistani Girl - ₹49", "callback_data": "pkg_7"}],
            [{"text": "❤️ 08 Sister & Brother - ₹30", "callback_data": "pkg_8"}],
            [
                {"text": "🎬 WATCH BIG FREE DEMOS", "callback_data": "btn_demo"},
                {"text": "💬 HELP & SUPPORT", "callback_data": "btn_support"}
            ]
        ]
    }

@app.route('/')
def home():
    return "Telegram Bot Server is Running!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    
    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        user_name = msg.get("from", {}).get("first_name", "User")
        text = msg.get("text", "")
        
        if text.startswith("/setphoto") or (msg.get("photo") and msg.get("caption", "").startswith("/setphoto")):
            photo_obj = None
            if msg.get("photo"):
                photo_obj = msg["photo"][-1]
            elif msg.get("reply_to_message") and msg.get("reply_to_message", {}).get("photo"):
                photo_obj = msg["reply_to_message"]["photo"][-1]
                
            if photo_obj:
                save_photo_id(photo_obj["file_id"])
                send_telegram_message(chat_id, "✅ Success! Welcome banner photo update ho gayi hai.")
            else:
                send_telegram_message(chat_id, "❌ Kripya koi photo bhejiye ya photo par reply karke `/setphoto` likhiye.")
            return "OK", 200

        if text.startswith("/start"):
            welcome_text = f"❤️❤️❤️ Hello **{user_name}**! ✨\n\nWelcome to **All Max Content Bot**\n\nSelect a package below to purchase:"
            reply_markup = get_main_menu_keyboard()
            saved_photo = get_saved_photo()
            
            if saved_photo:
                res = send_telegram_photo(chat_id, saved_photo, welcome_text, reply_markup)
                if not res.get("ok"):
                    send_telegram_message(chat_id, welcome_text, reply_markup)
            else:
                send_telegram_message(chat_id, welcome_text, reply_markup)
            return "OK", 200

    elif "callback_query" in data:
        query = data["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        message_id = query["message"]["message_id"]
        user_name = query.get("from", {}).get("first_name", "User")
        data_val = query["data"]
        
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})

        if data_val == "main_menu":
            welcome_text = f"❤️❤️❤️ Hello **{user_name}**! ✨\n\nWelcome to **All Max Content Bot**\n\nSelect a package below to purchase:"
            reply_markup = get_main_menu_keyboard()
            edit_message_text(chat_id, message_id, welcome_text, reply_markup)
            return "OK", 200

        if data_val == "btn_demo":
            send_telegram_message(chat_id, "🎬 Yeh raha aapka demo content link:\n\n🔗 https://t.me/+iLoNw5R4Qwk5MGI1")
            return "OK", 200

        if data_val == "btn_support":
            send_telegram_message(chat_id, "🛠 Kisi bhi madad ke liye yahan contact karein:\n\n🔗 https://t.me/your_support_username")
            return "OK", 200

        if data_val in PACKAGES:
            pkg = PACKAGES[data_val]
            payment_text = f"📦 **{pkg['name']}**\n💰 Price: **Rs.{pkg['price']}**\n\nClick the button below to complete your payment:"
            payment_keyboard = {
                "inline_keyboard": [
                    [{"text": f"Pay ₹{pkg['price']} Now", "url": pkg["payment_link"]}],
                    [{"text": "🔙 Back to Menu", "callback_data": "main_menu"}]
                ]
            }
            edit_message_text(chat_id, message_id, payment_text, payment_keyboard)
            return "OK", 200

    return "OK", 200

@app.route('/razorpay-webhook', methods=['POST'])
def razorpay_webhook():
    data = request.get_json()
    if data.get("event") == "payment_link.paid":
        payment_entity = data["payload"]["payment_link"]["entity"]
        notes = payment_entity.get("notes", {})
        telegram_id = notes.get("telegram_id")
        package_id = notes.get("package_id")
        
        if telegram_id and package_id in PACKAGES:
            pkg = PACKAGES[package_id]
            channel_link = pkg["content_link"]
            if channel_link:
                send_telegram_message(
                    telegram_id,
                    f"✅ **Payment Successful!**\n\nAapne **{pkg['name']}** purchase kar liya hai.\n\nNiche diye gaye link se content access karein:\n\n🔗 {channel_link}"
                )
    return "OK", 200

if __name__ == '__main__':
    RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_EXTERNAL_URL:
        import urllib.request
        webhook_url = f"{RENDER_EXTERNAL_URL}/{TELEGRAM_BOT_TOKEN}"
        urllib.request.urlopen(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
            
