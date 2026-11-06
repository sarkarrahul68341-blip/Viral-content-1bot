import os
import razorpay
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Aapki Razorpay Test Keys
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

# Initialize Razorpay Client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

# Package Details (Name, Price in Rupees)
PACKAGES = {
    "pkg_1": {"name": "01 CP Video and File", "price": 249},
    "pkg_2": {"name": "02 Rap & CP & Big File VD", "price": 89},
    "pkg_3": {"name": "03 Mom and Son Real Sex", "price": 45},
    "pkg_4": {"name": "04 Insta viral reels and sex", "price": 30},
    "pkg_5": {"name": "05 Ganga bath group join", "price": 199},
    "pkg_6": {"name": "06 CP Bath camera hidden", "price": 55},
    "pkg_7": {"name": "07 Pakistani girl real fuke", "price": 49},
    "pkg_8": {"name": "08 Sister and brother sex", "price": 30},
}

# Start Command - Show Menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔑 01 CP Video and File --------- Rs.249", callback_data="pkg_1")],
        [InlineKeyboardButton("🔑 02 Rap & CP & Big File VD --------- Rs.89", callback_data="pkg_2")],
        [InlineKeyboardButton("🔑 03 Mom and Son Real Sex --------- Rs.45", callback_data="pkg_3")],
        [InlineKeyboardButton("🔞 04 Insta viral reels and sex --------- Rs.30", callback_data="pkg_4")],
        [InlineKeyboardButton("🔥 05 Ganga bath group join --------- Rs.199", callback_data="pkg_5")],
        [InlineKeyboardButton("🔥 06 CP Bath camera hidden --------- Rs.55", callback_data="pkg_6")],
        [InlineKeyboardButton("🔥 07 Pakistani girl real fuke --------- Rs.49", callback_data="pkg_7")],
        [InlineKeyboardButton("❤️ 08 Sister and brother sex --------- Rs.30", callback_data="pkg_8")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✨ **All Max Content Bot**\n\nSelect a package below to purchase:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Handle Button Click & Create Razorpay Payment Link
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data in PACKAGES:
        pkg = PACKAGES[data]
        amount_in_paise = pkg["price"] * 100  # Razorpay takes amount in paise

        try:
            # Create a Razorpay Payment Link
            payment_link = client.payment_link.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "accept_partial": False,
                "description": pkg["name"],
                "customer": {
                    "name": "Customer",
                    "email": "customer@example.com",
                    "contact": "9999999999"
                },
                "notify": {"sms": False, "email": False},
                "reminder_enable": False,
                "callback_url": "https://t.me/",
                "callback_method": "get"
            })

            payment_url = payment_link.get("short_url")
            
            keyboard = [[InlineKeyboardButton(f"Pay ₹{pkg['price']} Now", url=payment_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                f"📦 **{pkg['name']}**\n💰 Price: **Rs.{pkg['price']}**\n\nClick the button below to complete your payment:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            await query.message.reply_text(f"Error creating payment link: {str(e)}")

@app.route('/')
def home():
    return "Telegram Bot & Razorpay Server is Running!"

# Webhook to receive payment success from Razorpay
@app.route('/razorpay-webhook', methods=['POST'])
def webhook():
    data = request.json
    # Payment success hone par yahan se file deliver karne ka logic aayega
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
    
