import telebot
import os
from keep_alive import keep_alive

# Render ya environment se token lene ke liye (agar token direct daalna ho toh 'YOUR_BOT_TOKEN' ki jagah rakh sakte hain)
TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Your bot is live and running successfully!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    # Flask server ko background mein chalu rakhne ke liye keep_alive call kiya hai
    keep_alive()
    bot.infinity_polling()
