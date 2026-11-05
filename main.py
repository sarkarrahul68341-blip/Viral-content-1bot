import os
from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Telegram Bot Token & Admin ID Setup (Updated with new token)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "9094967544:AAHiB3IEVow4A5JRl4BIdt4HijZwHYR_qE4")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456789"))

bot = telebot.TeleBot(BOT_TOKEN)

# Flask Keep-Alive Server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

PRODUCTS = {
    "prod_1": {
        "name": "Premium Pack 1 (Video & File)",
        "price": "₹199",
        "file_url": "https://example.com/your-video-or-file.zip"
    }
}

@bot.message_handler(commands=['start'])
def start_cmd(message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🛍️ Buy Premium Video & File (₹199)", callback_data="buy_prod_1"))
    
    welcome_msg = (
        "👋 **Welcome to Our Official Digital Store!**\n\n"
        "Niche diye gaye button par click karke product select karein aur payment karein."
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=kb, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def process_buy(call):
    prod_id = call.data.replace("buy_", "")
    product = PRODUCTS.get(prod_id)
    
    if product:
        upi_details = (
            f"🛒 **Product:** {product['name']}\n"
            f"💰 **Amount:** {product['price']}\n\n"
            "📌 **Payment Instructions:**\n"
            "1. Niche diye gaye UPI ID par payment karein:\n"
            "   `apka-upi-id@okhdfcbank`\n"
            "2. Payment karne ke baad UTR/Transaction ID ya screenshot is chat mein bhej dein."
        )
        bot.send_message(call.message.chat.id, upi_details, parse_mode="Markdown")

@bot.message_handler(content_types=['photo', 'text'])
def handle_payment_proof(message):
    if message.chat.id == ADMIN_ID:
        return

    user_info = f"👤 **User:** @{message.from_user.username} (ID: `{message.chat.id}`)"
    
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ Approve & Send Content", callback_data=f"approve_{message.chat.id}_prod_1"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.chat.id}")
    )

    bot.send_message(ADMIN_ID, f"📩 **New Payment Proof Received!**\n{user_info}")
    
    if message.content_type == 'photo':
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    else:
        bot.send_message(ADMIN_ID, f"Transaction Note/UTR: {message.text}")
        
    bot.send_message(ADMIN_ID, "Action lein:", reply_markup=kb)
    bot.reply_to(message, "✅ Aapka payment proof receive ho gaya hai! Verification ke baad content mil jayega.")

@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def process_admin_action(call):
    data = call.data.split("_")
    action = data[0]
    user_id = int(data[1])

    if action == "approve":
        prod_id = data[2]
        product = PRODUCTS.get(prod_id)
        
        delivery_msg = f"🎉 **Payment Verified!**\n\nYeh raha aapka digital content:\n{product['file_url']}"
        bot.send_message(user_id, delivery_msg, parse_mode="Markdown")
        
        bot.answer_callback_query(call.id, "Product Delivered Successfully!")
        bot.edit_message_text(f"✅ Approved & Delivered to ID: {user_id}", call.message.chat.id, call.message.message_id)

    elif action == "reject":
        bot.send_number = bot.send_message(user_id, "❌ Aapka payment verify nahi ho paya. Kripya sahi UTR ya clear screenshot dobara bhej dein.")
        bot.answer_callback_query(call.id, "Rejected.")
        bot.edit_message_text(f"❌ Rejected for ID: {user_id}", call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
