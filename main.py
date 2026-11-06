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

BOT_TOKEN = "9094967544:AAGeMcK8UZoYlaCQOqnR7PuXA2msFmJn-9Q"
UPI_ID = "puja6489@ptyes"
SUPPORT_TELEGRAM_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
WELCOME_PHOTO_URL = "https://raw.githubusercontent.com/sarkarrahul/Viral-content-1bot/main/Indian-GF-Videos-porn-site.jpg"

WELCOME_HEADING = (
    "❤️ Welcome to Viral Desi MMS Content Bot ❤️\n\n"
    "Niche diye gaye menu se apna pasandida package ya demo select karein:"
)

CONTENT_DATABASE = {
    "item_1": {"title": "🔑 01 CP Video and File", "price": "Rs.249"},
    "item_2": {"title": "🔑 02 Rap & CP & Big File VD", "price": "Rs.89"},
    "item_3": {"title": "🔑 03 Mom and son Real sex", "price": "Rs.45"},
    "item_4": {"title": "🔞 04 Insta viral reels and sex", "price": "Rs.30"},
    "item_5": {"title": "🔥 05 Ganga bath group join", "price": "Rs.199"},
    "item_6": {"title": "🔥 06 CP Bath camera hidden", "price": "Rs.55"},
    "item_7": {"title": "🔥 07 pakistani girl real fuke", "price": "Rs.49"},
    "item_8": {"title": "❤️ 08 sister and brother sex", "price": "Rs.30"},
}

DEMO_DATABASE = {
    "demo_1": {
        "title": "🎥 Watch Free Demo 1",
        "url": "https://t.me/+f9i3BlsoUeZiZmY1",
    },
    "demo_2": {
        "title": "🎥 Watch Free Demo 2",
        "url": "https://t.me/+w4MJrYfZ2zIyMTQ1",
    },
    "demo_3": {
        "title": "🎥 Watch Free Demo 3",
        "url": "https://t.me/+v_jJUbh_U7M3OGQ1",
    },
    "demo_4": {
        "title": "🎥 Watch Free Demo 4",
        "url": "https://t.me/+s4Zzmwni59diNjU1",
    },
}

app_web = Flask(__name__)


@app_web.route("/")
def home():
  return "Bot is running live 24/7!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app_web.run(host="0.0.0.0", port=port)def get_main_menu_keyboard():
  keyboard = []
  for key, data in CONTENT_DATABASE.items():
    t_label = data["title"] + " -------- " + data["price"]
    c_data = "buy_" + key
    btn = InlineKeyboardButton(t_label, callback_data=c_data)
    keyboard.append([btn])

  demo_btn = InlineKeyboardButton(
      "🎥 Watch Free Demo", callback_data="open_demos"
  )
  keyboard.append([demo_btn])

  supp_btn = InlineKeyboardButton(
      "💬 Help & Support", url=SUPPORT_TELEGRAM_LINK
  )
  keyboard.append([supp_btn])

  return InlineKeyboardMarkup(keyboard)


def get_demo_menu_keyboard():
  keyboard = []
  for key, data in DEMO_DATABASE.items():
    d_label = data["title"]
    d_url = data["url"]
    btn = InlineKeyboardButton(d_label, url=d_url)
    keyboard.append([btn])

  back_btn = InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")
  keyboard.append([back_btn])

  return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  reply_markup = get_main_menu_keyboard()
  try:
    await context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=WELCOME_PHOTO_URL,
        caption=WELCOME_HEADING,
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )
  except Exception:
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=WELCOME_HEADING,
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  data = query.data

  if data == "back_home":
    reply_markup = get_main_menu_keyboard()
    try:
      await query.message.edit_caption(
          caption=WELCOME_HEADING,
          reply_markup=reply_markup,
          parse_mode="Markdown",
      )
    except Exception:
      await query.message.reply_text(
          text=WELCOME_HEADING,
          reply_markup=reply_markup,
          parse_mode="Markdown",
      )

  elif data == "open_demos":
    demo_heading = (
        "🎬 **Free Demo Videos Collection**\n\n"
        "Niche diye gaye demo links par click karke aap videos dekh sakte hain:"
    )
    reply_markup = get_demo_menu_keyboard()
    try:
      await query.message.edit_caption(
          caption=demo_heading,
          reply_markup=reply_markup,
          parse_mode="Markdown",
      )
    except Exception:
      await query.message.reply_text(
          text=demo_heading,
          reply_markup=reply_markup,
          parse_mode="Markdown",
      )

  elif data.startswith("buy_"):
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

    back_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]]
    )

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=payment_text,
        reply_markup=back_keyboard,
        parse_mode="Markdown",
    )


def main():
  try:
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("OK")
    app.run_polling()
  except Exception as e:
    print("ERROR:")
    traceback.print_exc()


if __name__ == "__main__":
  main()
