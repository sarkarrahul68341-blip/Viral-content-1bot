import os
import subprocess
import sys
import traceback

try:
  import telegram
  import flask
except ImportError:
  subprocess.check_call([
      sys.executable,
      "-m",
      "pip",
      "install",
      "python-telegram-bot",
      "flask",
  ])

import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# --- CONFIGURATIONS ---
BOT_TOKEN = "9094967544:AAHk7zir2JbhHAQStB6BtcMFai4HbvwHQOQ"
UPI_ID = "puja6489@ptyes"
SUPPORT_TELEGRAM_LINK = "https://t.me/YourSupportUsername"

WELCOME_PHOTO_URL = "https://picsum.photos/800/500"
WELCOME_HEADING = (
    "❤️ **Welcome to Viral Desi MMS Content Bot** ❤️\n\nNiche diye gaye menu se"
    " apna pasandida package select karein:"
)

# --- 8 CONTENT PACKAGES DATABASE ---
CONTENT_DATABASE = {
    "item_1": {
        "title": "🔑 01 CP Video and File",
        "price": "Rs.249",
    },
    "item_2": {
        "title": "🔑 02 Rap & CP & Big File VD",
        "price": "Rs.89",
    },
    "item_3": {
        "title": "🔑 03 Mom and son Real sex",
        "price": "Rs.45",
    },
    "item_4": {
        "title": "🔞 04 Insta viral reels and sex",
        "price": "Rs.30",
    },
    "item_5": {
        "title": "🔥 05 Ganga bath group join",
        "price": "Rs.199",
    },
    "item_6": {
        "title": "🔥 06 CP Bath camera hidden",
        "price": "Rs.55",
    },
    "item_7": {
        "title": "🔥 07 pakistani girl real fuke",
        "price": "Rs.49",
    },
    "item_8": {
        "title": "❤️ 08 sister and brother sex",
        "price": "Rs.30",
    },
}

# --- RENDER KEEP-ALIVE SERVER ---
app_web = Flask(__name__)


@app_web.route("/")
def home():
  return "Bot is running live 24/7!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app_web.run(host="0.0.0.0", port=port)


# --- TELEGRAM BOT LOGIC ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = []
  for key, data in CONTENT_DATABASE.items():
    keyboard.append([
        InlineKeyboardButton(
            f"{data['title']} -------- {data['price']}",
            callback_data=f"buy_{key}",
        )
    ])
  keyboard.append([
      InlineKeyboardButton("💬 Help & Support", url=SUPPORT_TELEGRAM_LINK)
  ])

  reply_markup = InlineKeyboardMarkup(keyboard)
  await context.bot.send_photo(
      chat_id=update.message.chat_id,
      photo=WELCOME_PHOTO_URL,
      caption=WELCOME_HEADING,
      reply_markup=reply_markup,
      parse_mode="Markdown",
  )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  data = query.data

  if data.startswith("buy_"):
    item_key = data.replace("buy_", "")
    item = CONTENT_DATABASE[item_key]

    payment_text = (
        f"🛍 **{item['title']}**\n"
        f"💰 **Price:** {item['price']}\n\n"
        "1️⃣ **Payment Karein:** Is UPI ID par payment bhejein:\n"
        f"`{UPI_ID}`\n\n"
        "2️⃣ **Screenshot Bhejein:** Payment karne ke baad screenshot is chat"
        " mein bhej dein. Verification ke baad aapko channel link mil jayega!"
    )
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=payment_text,
        parse_mode="Markdown",
    )


def main():
  try:
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Business Telegram Bot with Web Server is running...")
    app.run_polling()
  except Exception as e:
    print("CRITICAL ERROR DURING STARTUP:")
    traceback.print_exc()


if __name__ == "__main__":
  main()
