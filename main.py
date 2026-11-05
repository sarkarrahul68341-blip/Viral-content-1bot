import os
from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= CONFIGURATION & SETTINGS =================
BOT_TOKEN = "9094967544:AAHiB3IEVow4A5JRl4BIdt4HijZwHYR_qE4"
ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456789")) # Apna Telegram Admin User ID yha daalein

# Yahan aap apna custom welcome message set kar sakti hain jo /start dabate hi sabko milega
WELCOME_MESSAGE = (
    "Hello everyone ❤️\n\n"
    "Welcome to our official digital store! "
    "Niche diye gaye buttons se apna pasandida product select karein aur payment karein."
)

# Aapka UPI ID yahan set rahega jisme payments aayengi
UPI_ID = "apka-upi-id@okhdfcbank"

# Products/Features list (Yahan aap multiple products, unke naam, price aur deliver hone wala content/link edit kar sakti hain)
PRODUCTS = {
    "prod_1": {
        "name": "🎬 Premium Video Pack",
        "price": "₹199",
        "file_url": "https://example.com/your-video-link.mp4"
    },
    "prod_2": {
        "name": "📸 Exclusive Photo & Audio Bundle",
        "price": "₹299",
        "file_url": "https://example.com/your-media-link.zip"
    }
}
# ============================================================

bot = telebot.TeleBot(BOT_TOKEN)

# Flask Keep-Alive Server (Render ke liye taaki bot 24/7 active rahe)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# /start command handler
@bot.message_handler(commands=['start'])
def start_cmd(message):
    kb = InlineKeyboardMarkup(row_width=1)
    
    # Dynamic buttons generation (Aap jitne chahein products yahan add kar sakti hain)
    for prod_id, info in PRODUCTS.items():
        kb.add(InlineKeyboardButton(f"{info['name']} ({info['price']})", callback_data=f"buy_{prod_id}"))
    
    # Extra custom menu buttons agar aapko aur lagane hon
    kb.add(InlineKeyboardButton("📞 Contact Support / Admin", url="https://t.me/your_username"))

    bot.send_message(message.chat.id, WELCOME_MESSAGE, reply_markup=kb, parse_mode="Markdown")

# Product click hone par UPI aur payment details show karna
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def process_buy(call):
    prod_id = call.data.replace("buy_", "")
    product = PRODUCTS.get(prod_id)
    
    if product:
        payment_text = (
            f"🛒 **Selected Product:** {product['name']}\n"
            f"💰 **Amount to Pay:** {product['price']}\n\n"
            f"📌 **Payment Instructions:**\n"
            f"1. Niche diye gaye UPI ID par payment karein:\n"
            f"   `{UPI_ID}`\n"
            f"2. Payment complete karne ke baad **UTR/Transaction ID** ya payment ka **Screenshot** ishi chat mein bhej dein."
        )
        bot.send_message(call.message.chat.id, payment_text, parse_mode="Markdown")

# Users dwara bheje gaye payment proof (Screenshot / Text UTR) ko handle karna aur Admin ko bhejna
@bot.message_handler(content_types=['photo', 'text'])
def handle_payment_proof(message):
    if message.chat.id == ADMIN_ID:
        return

    user_info = f"👤 **User:** @{message.from_user.username} (ID: `{message.chat.id}`)"
    
    # Admin ke liye approval buttons
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
    bot.reply_to(message, "✅ Aapka payment proof successfully receive ho gaya hai! Admin verification ke baad aapko content mil jayega.")

# Admin dwara Approve ya Reject karne ka action handler
@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def process_admin_action(call):
    data = call.data.split("_")
    action = data[0]
    user_id = int(data[1])

    if action == "approve":
        prod_id = data[2] if len(data) > 2 else "prod_1"
        product = PRODUCTS.get(prod_id, PRODUCTS["prod_1"])
        
        delivery_msg = f"🎉 **Payment Verified Successfully!**\n\nYeh raha aapka digital content:\n{product['file_url']}"
        bot.send_message(user_id, delivery_msg, parse_mode="Markdown")
        
        bot.answer_callback_query(call.id, "Product Delivered Successfully!")
        bot.edit_message_text(f"✅ Approved & Delivered to ID: {user_id}", call.message.chat.id, call.message.message_id)

    elif action == "reject":
        bot.send_message(user_id, "❌ Aapka payment verify nahi ho paya. Kripya sahi UTR ya clear screenshot dobara bhej dein.")
        bot.answer_callback_query(call.id, "Rejected.")
        bot.edit_message_text(f"❌ Rejected for ID: {user_id}", call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
