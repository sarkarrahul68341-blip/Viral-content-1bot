import os
import razorpay
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Credentials (Ab yahan aapki nayi test keys set hain)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

# Initialize Razorpay Client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Buy Digital Content (₹10)", callback_data="buy_content")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Click below to purchase and receive your digital file automatically:",
        reply_markup=reply_markup
    )

# Handle Button Click & Create Razorpay Payment Link
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_content":
        try:
            # Create a Razorpay Payment Link for testing (Amount in paise: 1000 = ₹10)
            payment_link = client.payment_link.create({
                "amount": 1000,
                "currency": "INR",
                "accept_partial": False,
                "description": "Digital Content Purchase",
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
            
            keyboard = [[InlineKeyboardButton("Pay Now", url=payment_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "Click the button below to complete your test payment:",
                reply_markup=reply_markup
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
    
