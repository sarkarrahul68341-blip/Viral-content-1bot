import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# Secure Token Loading from Environment
TOKEN = os.environ.get('BOT_TOKEN', '9094967544:AAFkhj5QPoiP2clIBU3JyXAmlrql0YzZam4')
bot = telebot.TeleBot(TOKEN)

# Aapke Render ka live URL (Jab Render live URL de de, toh yahan update kar dena)
WEB_APP_URL = os.environ.get('WEB_APP_URL', 'https://your-bot-name.onrender.com')

# ----------------- FLASK SERVER (Keep-Alive) -----------------
app = Flask('')

@app.route('/')
def home():
    return "All-in-One Bot is running 24/7!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ----------------- TELEGRAM BOT INTERFACE -----------------

@bot.message_handler(commands=['start'])
def send_main_menu(message):
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    
    markup = types.InlineKeyboardMarkup()
    
    # All-in-One Mini App Hub Button
    web_app = types.WebAppInfo(url=WEB_APP_URL)
    
    markup.add(types.InlineKeyboardButton("🚀 Open All-in-One Hub", web_app=web_app))
    markup.add(types.InlineKeyboardButton("💬 Support", callback_data="support_menu"))
    
    text = (
        f"Hello {user_name} 🐣\n\n"
        "Welcome to your **All-in-One VIP Hub**! 💖\n\n"
        "💎 Yahan aapko sabhi plans, demos aur features ek hi jagah milenge.\n"
        "🎁 Niche diye gaye button par click karke Hub kholein:"
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "support_menu":
        bot.answer_callback_query(call.id, text="Support team se connect ho rahe hain...", show_alert=True)
        bot.send_message(call.message.chat.id, "💬 Kisi bhi sahayata ke liye yahan contact karein: @your_support_username")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
