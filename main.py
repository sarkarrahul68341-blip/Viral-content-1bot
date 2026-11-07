import os
import asyncio
import razorpay
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

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

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

# Single global event loop initialization for Telegram Bot
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()
loop.run_until_complete(telegram_app.initialize())

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

def get_reply_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🎬 Demo"), KeyboardButton("📢 Channel"), KeyboardButton("🛠 Support")]
    ], resize_keyboard=True)

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 01 CP Video - ₹249", callback_data="pkg_1")],
        [InlineKeyboardButton("🔑 02 Rap & Big File - ₹89", callback_data="pkg_2")],
        [InlineKeyboardButton("🔑 03 Mom & Son - ₹45", callback_data="pkg_3")],
        [InlineKeyboardButton("🔞 04 Insta Viral - ₹30", callback_data="pkg_4")],
        [InlineKeyboardButton("🔥 05 Ganga Bath - ₹199", callback_data="pkg_5")],
        [InlineKeyboardButton("🔥 06 CP Bath Hidden - ₹55", callback_data="pkg_6")],
        [InlineKeyboardButton("🔥 07 Pakistani Girl - ₹49", callback_data="pkg_7")],
        [InlineKeyboardButton("❤️ 08 Sister & Brother - ₹30", callback_data="pkg_8")],
    ])

async def start(update: Update, context):
    user = update.effective_user
    user_name = user.first_name if user and user.first_name else "User"
    reply_markup = get_main_menu_keyboard()
    reply_kb = get_reply_keyboard()
    welcome_text = f"❤️❤️❤️ Hello **{user_name}**! ✨\n\nWelcome to **All Max Content Bot**\n\nSelect a package below to purchase:"
    saved_photo = get_saved_photo()
    
    if update.message:
        await update.message.reply_text("👇 Menu options:", reply_markup=reply_kb)
        if saved_photo:
            try:
                await update.message.reply_photo(photo=saved_photo, caption=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
                return
            except Exception:
                pass
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        if saved_photo:
            try:
                await update.callback_query.message.edit_media(media=InputMediaPhoto(media=saved_photo, caption=welcome_text, parse_mode="Markdown"), reply_markup=reply_markup)
                return
            except Exception:
                pass
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def set_photo_handler(update: Update, context):
    message = update.message
    photo_obj = None
    if message.photo:
        photo_obj = message.photo[-1]
    elif message.reply_to_message and message.reply_to_message.photo:
        photo_obj = message.reply_to_message.photo[-1]
        
    if photo_obj:
        save_photo_id(photo_obj.file_id)
        await message.reply_text("✅ Success! Welcome banner photo update ho gayi hai. Ab naye users ko yahi photo dikhegi!")
    else:
        await message.reply_text("❌ Kripya koi photo bhejiye ya photo par reply karke `/setphoto` likhiye.")

async def handle_text_buttons(update: Update, context):
    text = update.message.text
    if text == "🎬 Demo":
        await update.message.reply_text("🎬 Yeh raha aapka demo content link:\n\n🔗 https://t.me/+iLoNw5R4Qwk5MGI1")
    elif text == "📢 Channel":
        await update.message.reply_text("📢 Hamara official channel join karein:\n\n🔗 https://t.me/+iLoNw5R4Qwk5MGI1")
    elif text == "🛠 Support":
        await update.message.reply_text("🛠 Kisi bhi madad ke liye yahan contact karein:\n\n🔗 https://t.me/your_support_username")

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        user = update.effective_user
        user_name = user.first_name if user and user.first_name else "User"
        reply_markup = get_main_menu_keyboard()
        saved_photo = get_saved_photo()
        welcome_text = f"❤️❤️❤️ Hello **{user_name}**! ✨\n\nWelcome to **All Max Content Bot**\n\nSelect a package below to purchase:"
        
        if saved_photo:
            try:
                await query.message.edit_media(media=InputMediaPhoto(media=saved_photo, caption=welcome_text, parse_mode="Markdown"), reply_markup=reply_markup)
                return
            except Exception:
                pass
        await query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        payment_url = pkg["payment_link"]
        keyboard = [
            [InlineKeyboardButton(f"Pay ₹{pkg['price']} Now", url=payment_url)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        payment_text = f"📦 **{pkg['name']}**\n💰 Price: **Rs.{pkg['price']}**\n\nClick the button below to complete your payment:"
        
        try:
            await query.message.edit_caption(caption=payment_text, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception:
            await query.message.edit_text(payment_text, reply_markup=reply_markup, parse_mode="Markdown")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setphoto", set_photo_handler))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_buttons))

@app.route('/')
def home():
    return "Telegram Bot Webhook Server is Running!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, telegram_app.bot)
    
    # Use the same global event loop to process updates safely
    global loop
    future = asyncio.run_coroutine_threadsafe(telegram_app.process_update(update), loop)
    try:
        future.result(timeout=10)
    except Exception as e:
        print(f"Webhook processing error: {e}")
        
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
                import requests
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                    "chat_id": telegram_id,
                    "text": f"✅ **Payment Successful!**\n\nAapne **{pkg['name']}** purchase kar liya hai.\n\nNiche diye gaye link se content access karein:\n\n🔗 {channel_link}",
                    "parse_mode": "Markdown"
                })
    return "OK", 200

if __name__ == '__main__':
    RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_EXTERNAL_URL:
        import urllib.request
        webhook_url = f"{RENDER_EXTERNAL_URL}/{TELEGRAM_BOT_TOKEN}"
        urllib.request.urlopen(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
        
