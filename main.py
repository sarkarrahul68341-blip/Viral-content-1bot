import os
import requests
import razorpay
from flask import Flask, request

TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
app = Flask(__name__)

PACKAGES = {
    "pkg_1": {"name": "01 CP Video and File", "price": 1, "link": "https://t.me/+iLoNw5R4Qwk5MGI1"},
    "pkg_2": {"name": "02 Rap & CP & Big File VD", "price": 89, "link": ""},
    "pkg_3": {"name": "03 Mom and Son Real Sex", "price": 45, "link": ""},
    "pkg_4": {"name": "04 Insta viral reels and sex", "price": 30, "link": ""},
    "pkg_5": {"name": "05 Ganga bath group join", "price": 199, "link": ""},
    "pkg_6": {"name": "06 CP Bath camera hidden", "price": 55, "link": ""},
    "pkg_7": {"name": "07 Pakistani girl real fuke", "price": 49, "link": ""},
    "pkg_8": {"name": "08 Sister and brother sex", "price": 30, "link": ""},
}

def send_telegram_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def edit_telegram_message(chat_id, message_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error editing message: {e}")

@app.route('/')
def home():
    return "Telegram Bot Webhook Server is Running!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    
    # Handle /start command or normal messages
    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        
        if text.startswith("/start"):
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🔑 01 CP Video and File --------- Rs.1 (Test)", "callback_data": "pkg_1"}],
                    [{"text": "🔑 02 Rap & CP & Big File VD --------- Rs.89", "callback_data": "pkg_2"}],
                    [{"text": "🔑 03 Mom and Son Real Sex --------- Rs.45", "callback_data": "pkg_3"}],
                    [{"text": "🔞 04 Insta viral reels and sex --------- Rs.30", "callback_data": "pkg_4"}],
                    [{"text": "🔥 05 Ganga bath group join --------- Rs.199", "callback_data": "pkg_5"}],
                    [{"text": "🔥 06 CP Bath camera hidden --------- Rs.55", "callback_data": "pkg_6"}],
                    [{"text": "🔥 07 Pakistani girl real fuke --------- Rs.49", "callback_data": "pkg_7"}],
                    [{"text": "❤️ 08 Sister and brother sex --------- Rs.30", "callback_data": "pkg_8"}]
                ]
            }
            send_telegram_message(chat_id, "✨ **All Max Content Bot**\n\nSelect a package below to purchase:", keyboard)

    # Handle button clicks (Callback Queries)
    elif "callback_query" in data:
        query = data["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        message_id = query["message"]["message_id"]
        data_key = query["data"]
        
        if data_key == "main_menu":
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🔑 01 CP Video and File --------- Rs.1 (Test)", "callback_data": "pkg_1"}],
                    [{"text": "🔑 02 Rap & CP & Big File VD --------- Rs.89", "callback_data": "pkg_2"}],
                    [{"text": "🔑 03 Mom and Son Real Sex --------- Rs.45", "callback_data": "pkg_3"}],
                    [{"text": "🔞 04 Insta viral reels and sex --------- Rs.30", "callback_data": "pkg_4"}],
                    [{"text": "🔥 05 Ganga bath group join --------- Rs.199", "callback_data": "pkg_5"}],
                    [{"text": "🔥 06 CP Bath camera hidden --------- Rs.55", "callback_data": "pkg_6"}],
                    [{"text": "🔥 07 Pakistani girl real fuke --------- Rs.49", "callback_data": "pkg_7"}],
                    [{"text": "❤️ 08 Sister and brother sex --------- Rs.30", "callback_data": "pkg_8"}]
                ]
            }
            edit_telegram_message(chat_id, message_id, "✨ **All Max Content Bot**\n\nSelect a package below to purchase:", keyboard)
            
        elif data_key in PACKAGES:
            pkg = PACKAGES[data_key]
            amount_in_paise = pkg["price"] * 100

            try:
                payment_link = client.payment_link.create({
                    "amount": amount_in_paise,
                    "currency": "INR",
                    "accept_partial": False,
                    "description": pkg["name"],
                    "customer": {
                        "name": "Customer",
                        "email": "customer@example.com",
                        "contact": "9876543210"
                    },
                    "notes": {
                        "telegram_id": chat_id,
                        "package_id": data_key
                    },
                    "notify": {"sms": False, "email": False},
                    "reminder_enable": False,
                    "callback_url": "https://t.me/",
                    "callback_method": "get"
                })

                payment_url = payment_link.get("short_url")
                
                keyboard = {
                    "inline_keyboard": [
                        [{"text": f"Pay ₹{pkg['price']} Now", "url": payment_url}],
                        [{"text": "🔙 Back to Menu", "callback_data": "main_menu"}]
                    ]
                }
                
                edit_telegram_message(
                    chat_id, 
                    message_id, 
                    f"📦 **{pkg['name']}**\n💰 Price: **Rs.{pkg['price']}**\n\nClick the button below to complete your payment:", 
                    keyboard
                )
            except Exception as e:
                edit_telegram_message(chat_id, message_id, f"Error creating payment link: {str(e)}")

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
            channel_link = pkg["link"]
            
            if channel_link:
                msg_text = f"✅ **Payment Successful!**\n\nAapne **{pkg['name']}** purchase kar liya hai.\n\nNiche diye gaye link se content access karein:\n\n🔗 {channel_link}"
                send_telegram_message(telegram_id, msg_text)
            
    return "OK", 200

if __name__ == '__main__':
    RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_EXTERNAL_URL:
        import urllib.request
        webhook_url = f"{RENDER_EXTERNAL_URL}/{TELEGRAM_BOT_TOKEN}"
        urllib.request.urlopen(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
