import os
import razorpay
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

PACKAGES = {
    # Test ke liye price 1 kar diya hai
    "pkg_1": {"name": "01 CP Video and File", "price": 1, "link": "https://t.me/+iLoNw5R4Qwk5MGI1"},
    "pkg_2": {"name": "02 Rap & CP & Big File VD", "price": 89, "link": ""},
    "pkg_3": {"name": "03 Mom and Son Real Sex", "price": 45, "link": ""},
    "pkg_4": {"name": "04 Insta viral reels and sex", "price": 30, "link": ""},
    "pkg_5": {"name": "05 Ganga bath group join", "price": 199, "link": ""},
    "pkg_6": {"name": "06 CP Bath camera hidden", "price": 55, "link": ""},
    "pkg_7": {"name": "07 Pakistani girl real fuke", "price": 49, "link": ""},
    "pkg_8": {"name": "08 Sister and brother sex", "price": 30, "link": ""},
}

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 01 CP Video and File --------- Rs.1 (Test)", callback_data="pkg_1")],
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
                    "telegram_id": query.message.chat_id,
                    "package_id": data
                },
                "notify": {"sms": False, "email": False},
                "reminder_enable": False,
                "callback_url": "https://t.me/",
                "callback_method": "get"
            })

            payment_url = payment_link.get("short_url")
            
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
        except Exception as e:
            await query.message.edit_text(f"Error creating payment link: {str(e)}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

@app.route('/')
def home():
    return "Telegram Bot Webhook Server is Running!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, telegram_app.bot)
    
    import asyncio
    async def process():
        await telegram_app.initialize()
        await telegram_app.process_update(update)
    
    asyncio.run(process())
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
                import asyncio
                async def send_content():
                    await telegram_app.initialize()
                    await telegram_app.bot.send_message(
                        chat_id=telegram_id,
                        text=f"✅ **Payment Successful!**\n\nAap
