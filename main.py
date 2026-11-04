import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# Bot Token from Environment
TOKEN = os.environ.get('BOT_TOKEN', '9094967544:AAFkhj5QPoiP2clIBU3JyXAmlrql0YzZam4')
bot = telebot.TeleBot(TOKEN)

# ----------------- FLASK SERVER (Keep-Alive for Render) -----------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ----------------- TELEGRAM BOT HANDLERS -----------------

# 1. Start Command / Main Menu (Folder Style)
@bot.message_handler(commands=['start'])
def send_main_menu(message):
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📁 Videos & Demos", callback_data="folder_videos"),
        types.InlineKeyboardButton("💎 VIP Plans", callback_data="folder_plans"),
        types.InlineKeyboardButton("💬 Support", callback_data="support")
    )
    
    text = (
        f"Hello {user_name} 🐣\n\n"
        "📂 **Main Menu (Home Folder)**\n"
        "Niche diye gaye folders mein se koi ek select karein:"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# 2. Folder Navigation (Button Clicks)
@bot.callback_query_handler(func=lambda call: True)
def handle_folders(call):
    if call.data == "folder_videos":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📁 **Videos Folder**\nAapke demos aur videos yahan available hain.",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    
    elif call.data == "folder_plans":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📁 **VIP Plans Folder**\nSabhi plans ki details yahan hain.",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        
    elif call.data == "back_home":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📁 Videos & Demos", callback_data="folder_videos"),
            types.InlineKeyboardButton("💎 VIP Plans", callback_data="folder_plans"),
            types.InlineKeyboardButton("💬 Support", callback_data="support")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📂 **Main Menu (Home Folder)**\nNiche diye gaye folders mein se koi ek select karein:",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        
    elif call.data == "support":
        bot.answer_callback_query(call.id, text="Opening support...")
        bot.send_message(call.message.chat.id, "💬 Support ke liye contact karein: @your_support_username")

# 3. Smart Auto-Reply for Normal Text Messages (Including Adult/VIP Queries)
@bot.message_handler(func=lambda message: True)
def smart_auto_reply(message):
    user_text = message.text.lower()
    
    # Agar koi adult ya vip content maange
    if any(word in user_text for word in ["adult", "vip", "private", "hot", "video", "content"]):
        bot.reply_to(message, "🔥 Haan, exclusive content available hai! Access karne ke liye niche diye gaye menu par click karein: /start")
    
    # Agar user hi/hello bole
    elif "hi" in user_text or "hello" in user_text or "hey" in user_text:
        bot.reply_to(message, "👋 Hello! Menu kholne ke liye /start type karein.")
    
    # Agar user price ya plan puche
    elif "price" in user_text or "plan" in user_text or "rate" in user_text:
        bot.reply_to(message, "💎 VIP plans aur details ke liye /start command bhejein.")
    
    # Baaki kisi bhi message par default auto-reply
    else:
        bot.reply_to(message, "🤖 Dhanyawad! Aapka message mil gaya hai. Menu dekhne ke liye /start dabayein.")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
