import os
from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =====================================================================
# 🛠️ MENU & BOT BUILDER PANEL (Yahan aap sab kuch edit kar sakti hain)
# =====================================================================

# 1. Telegram Bot Token & Admin ID
BOT_TOKEN = "9094967544:AAHiB3IEVow4A5JRl4BIdt4HijZwHYR_qE4"
ADMIN_ID = 123456789  # ⚠️ Yahan apna Telegram Admin User ID daal dein

# 2. Start Message (Jo user /start dabate hi sabse pehle dekhega)
WELCOME_MESSAGE = (
    "Hello everyone ❤️\n\n"
    "✨ **Welcome to Our Official Digital Store!** ✨\n"
    "Niche diye gaye menu se apna pasandida product ya feature select karein:"
)

# 3. Aapka Payment UPI ID (Jisme saari payments aayengi)
UPI_ID = "apka-upi-id@okhdfcbank"

# 4. Menu & Products Builder (Yahan aap apne buttons, price aur delivery link add/edit kar sakti hain)
# Aap yahan 30 tak ya jitne chahein utne items add kar sakti hain.
MENU_ITEMS = {
    "item_1": {
        "title": "🎬 Premium Video Pack (₹199)",
        "price": "₹199",
        "type": "digital", # digital content delivery
        "file_url": "https://example.com/your-video-link.mp4"
    },
    "item_2": {
        "title": "📸 Exclusive Photo & Audio Bundle (₹299)",
        "price": "₹299",
        "type": "digital",
        "file_url": "https://example.com/your-media-link.zip"
    },
    "item_3": {
        "title": "🚀 VIP Channel Access (₹499)",
        "price": "₹499",
        "type": "digital",
        "file_url": "https://t.me/+your_invite_link"
    }
}
# =====================================================================

bot = telebot.TeleBot(BOT_TOKEN)

# Flask Keep-Alive Server for Render (24/7 uptime)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# /start command handler (Menu Builder layout)
@bot.message_handler(commands=['start'])
def start_cmd(message):
    kb = InlineKeyboardMarkup(row_width=1) # Buttons ek ke niche ek aayenge (Line by line)
    
    # Menu builder items ko buttons mein convert karna
    for key, item in MENU_ITEMS.items():
        kb.add(InlineKeyboardButton(item["title"], callback_data=f"select_{key}"))
    
    # Extra support button
    kb.add(InlineKeyboardButton("📞 Contact Admin / Support", url=f"t.me/your_username"))

    bot.send_message(message.chat.id, WELCOME_MESSAGE, reply_markup=kb, parse_mode="Markdown")

# Menu button click hone par UPI aur payment details show karna
@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def process_menu_selection(call):
    item_key = call.data.replace("select_", "")
    item = MENU_ITEMS.get(item_key)
    
    if item:
        payment_text = (
            f"🛒 **Selected Item:** {item['title']}\n"
            f"💰 **Price:** {item['price']}\n\n"
            f"📌 **Payment Instructions:**\n"
            f"1. Is UPI ID par payment karein:\n"
            f"   `{UPI_ID}`\n"
            f"2. Payment karne ke baad **UTR/Transaction ID** ya payment ka **Screenshot** isi chat mein bhej dein."
        )
        # Store selected item in state via callback data tracking in approval
        bot.send_message(call.message.chat.id, payment_text, parse_mode="Markdown")

# User dwara bheje gaye payment proof (Screenshot ya UTR text) ko handle karna
@bot.message_handler(content_types=['photo', 'text'])
def handle_payment_proof(message):
    if message.chat.id == ADMIN_ID:
        return

    user_info = f"👤 **User:** @{message.from_user.username} (ID: `{message.chat.id}`)"
    
    # Admin ke liye approval buttons (Approve / Reject)
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ Approve & Send Content", callback_data=f"approve_{message.chat.id}_item_1"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.chat.id}")
    )

    bot.send_message(ADMIN_ID, f"📩 **New Payment Proof Received!**\n{user_info}")
    
    if message.content_type == 'photo':
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    else:
        bot.send_message(ADMIN_ID, f"Transaction Note/UTR: {message.text}")
        
    bot.send_message(ADMIN_ID, "Action lein:", reply_markup=kb)
    bot.reply_to(message, "✅ Aapka payment proof successfully receive ho gaya hai! Verification ke baad aapko content mil jayega.")

# Admin action handler (Approve/Reject)
@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def process_admin_action(call):
    data = call.data.split("_")
    action = data[0]
    user_id = int(data[1])

    if action == "approve":
        item_key = data[2] if len(data) > 2 else "item_1"
        item = MENU_ITEMS.get(item_key, MENU_ITEMS["item_1"])
        
        delivery_msg = f"🎉 **Payment Verified Successfully!**\n\nYeh raha aapka digital content:\n{item['file_url']}"
        bot.send_message(user_id, delivery_msg, parse_mode="Markdown")
        
        bot.answer_callback_query(call.id, "Content Delivered!")
        bot.edit_message_text(f"✅ Approved & Delivered to ID: {user_id}", call.message.chat.id, call.message.message_id)

    elif action == "reject":
        bot.send_message(user_id, "❌ Aapka payment verify nahi ho paya. Kripya sahi UTR ya clear screenshot dobara bhej dein.")
        bot.answer_callback_query(call.id, "Rejected.")
        bot.edit_message_text(f"❌ Rejected for ID: {user_id}", call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
