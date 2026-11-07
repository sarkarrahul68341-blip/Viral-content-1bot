import os
import asyncio
import razorpay
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

# Telegram Application Build
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

# Server startup par hi bot ko initialize kar lo taaki baad mein delay na ho
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(telegram_app.initialize())

# Packages Mapping
PACKAGES = {
    "pkg_1": {"name": "01 CP Video and File", "price": 249, "payment_link": "https://rzp.io/l/testlink", "content_link": "https://t.me/+iLoNw5R4Qwk5MGI1"},
    "pkg_2": {"name": "02 Rap & CP & Big File VD", "price": 89, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_3": {"name": "03 Mom and Son Real Sex", "price": 45, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_4": {"name": "04 Insta viral reels and sex", "price": 30, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_5": {"name": "05 Ganga bath group join", "price": 199, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_6": {"name": "06 CP Bath camera hidden", "price": 55, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_7": {"name": "07 Pakistani girl real fuke", "price": 49, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_8": {"name": "08 Sister and brother sex", "price": 30, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
}

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 01 CP Video and File --------- Rs.249", callback_data="pkg_1")],
        [InlineKeyboardButton("🔑 02 Rap & CP & Big File VD --------- Rs.89", callback_data="pkg_2")],
        [InlineKeyboardButton("🔑 03 Mom and Son Real Sex --------- Rs.45", callback_data="pkg_3")],
        [InlineKeyboardButton("🔞 04 Insta viral reels and sex --------- Rs.30", callback_data="pkg_4")],
        [InlineKeyboardButton("🔥 05 Ganga bath group join --------- Rs.199", callback_data="pkg_5")],
        [InlineKeyboardButton("🔥 06 CP Bath camera hidden --------- Rs.55", callback_data="pkg_6")],
        [InlineKeyboardButton("🔥 07 Pakistani girl real fuke --------- Rs.49", callback_data="pkg_7")],
        [InlineKeyboardButton("❤️ 08 Sister and brother sex --------- Rs.30", callback_data="pkg_8")],
    ])

async def start(update: Update, context):
    reply_markup = get_main_menu_keyboard()
    if update.callback_query:
        await update.callback_query.message.edit_text(
            "✨ **All Max Content Bot**\n\nSelect a package below to purchase:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "✨ **All Max Content Bot**\n\nSelect a package below to purchase:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "main_menu":
        await start(update, context)
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        payment_url = pkg["payment_link"]

        keyboard = [
            [InlineKeyboardButton(f"Pay ₹{pkg['price']} Now", url=payment_url)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.edit_text(
            f"📦 **{pkg['name']}**\n💰 Price: **Rs.{pkg['price']}**\n\nClick the button below to complete your payment:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

@app.route('/')
def home():
    return "Telegram Bot Webhook Server is Running!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, telegram_app.bot)
    
    req_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(req_loop)
    req_loop.run_until_complete(telegram_app.process_update(update))
    
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
                req_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(req_loop)
                req_loop.run_until_complete(
                    telegram_app.bot.send_message(
                        chat_id=telegram_id,
                        text=f"✅ **Payment Successful!**\n\nAapne **{pkg['name']}** purchase kar liya hai.\n\nNiche diye gaye link se content access karein:\n\n🔗 {channel_link}",
                        parse_mode="Markdown"
                    )
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
    
