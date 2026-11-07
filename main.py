import os
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from flask import Flask

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

# Minimal Flask app to satisfy Render port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot is Running via Polling!"

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

# Main menu keyboard: Packages + Left side Big Demo, Right side Help & Support
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
        # Left side: Demo, Right side: Help & Support
        [
            InlineKeyboardButton("🎬 WATCH BIG FREE DEMOS", callback_data="btn_demo"),
            InlineKeyboardButton("💬 HELP & SUPPORT", callback_data="btn_support")
        ]
    ])

async def start(update: Update, context):
    user = update.effective_user
    user_name = user.first_name if user and user.first_name else "User"
    reply_markup = get_main_menu_keyboard()
    
    welcome_text = f"❤️❤️❤️ Hello **{user_name}**! ✨\n\nWelcome to **All Max Content Bot**\n\nSelect a package below to purchase:"
    saved_photo = get_saved_photo()
    
    if update.message:
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

    if data == "btn_demo":
        await query.message.reply_text("🎬 Yeh raha aapka demo content link:\n\n🔗 https://t.me/+iLoNw5R4Qwk5MGI1")
        return

    if data == "btn_support":
        await query.message.reply_text("🛠 Kisi bhi madad ke liye yahan contact karein:\n\n🔗 https://t.me/your_support_username")
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

if __name__ == '__main__':
    # Run Flask in background thread for Render
    port = int(os.environ.get("PORT", 10000))
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True)
    flask_thread.start()

    # Run Telegram Bot via Polling (Super stable, no webhook/event loop crashes)
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setphoto", set_photo_handler))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running via polling...")
    application.run_polling()
        
