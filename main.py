import os
import subprocess
import sys
import traceback

# Automatic library installation check
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

# --- 1. APNI DETAILS YAHAN SET HAI ---
BOT_TOKEN = "9094967544:AAHk7zir2JbhHAQStB6BtcMFai4HbvwHQOQ"
UPI_ID = "puja6489@ptyes"
SUPPORT_TELEGRAM_LINK = "https://t.me/YourSupportUsername"

# --- 2. WELCOME BANNER PHOTO AUR TEXT ---
WELCOME_PHOTO_URL = "https://picsum.photos/800/500"
WELCOME_HEADING = "hello everyone ❤️❤️❤️\n\nWelcome to my official store! Niche diye gaye menu se content choose karein:"

# --- 3. PAID CONTENT DATABASE ---
CONTENT_DATABASE = {
    "item_1": {
        "title": "🔥 Premium Video Package 1",
        "price": "₹199",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "type": "video",
    },
    "item_2": {
        "title": "💎 Exclusive Photo Collection",
        "price": "₹99",
        "media_url": "https://picsum.photos/600/400",
        "type": "photo",
    },
}

# --- 4. 4 DEMO BUTTONS WITH INDIVIDUAL TELEGRAM LINKS ---
DEMO_BUTTONS = {
    "demo_1": {
        "title": "🎬 Demo Video 1",
        "url": "https://t.me/+s4Zzmwni59diNjU1",
    },
    "demo_2": {
        "title": "🎬 Demo Video 2",
        "url": "https://t.me/+f9i3BlsoUeZiZmY1",
    },
    "demo_3": {
        "title": "🎬 Demo Video 3",
        "url": "https://t.me/+w4MJrYfZ2zIyMTQ1",
    },
    "demo_4": {
        "title": "🎬 Demo Video 4",
        "url": "https://t.me/+v_jJUbh_U7M3OGQ1",
    },
}

# --- 5. RENDER KEEP-ALIVE SERVER (Flask) ---
app_web = Flask(__name__)


@app_web.route("/")
def home():
  return "Bot is running live 24/7!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app_web.run(host="0.0.0.0", port=port)


# Telegram Bot Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = []
  for key, data in CONTENT_DATABASE.items():
    keyboard.append([
        InlineKeyboardButton(
            f"{data['title']} — {data['price']}", callback_data=f"buy_{key}"
        )
    ])
  keyboard.append([
      InlineKeyboardButton("🎥 Watch Free Demo", callback_data="demo_menu")
  ])
  keyboard.append(
      [InlineKeyboardButton("💬 Help & Support", url=SUPPORT_TELEGRAM_LINK)]
  )

  reply_markup = InlineKeyboardMarkup(keyboard)
  await context.bot.send_photo(
      chat_id=update.message.chat_id,
      photo=WELCOME_PHOTO_URL,
      caption=WELCOME_HEADING,
      reply_markup=reply_markup,
  )


# Button Click Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  data = query.data

  # Free Demo Menu (List of 4 Buttons with Separate Telegram Links)
  if data == "demo_menu":
    demo_keyboard = []
    for d_key, d_data in DEMO_BUTTONS.items():
      demo_keyboard.append(
          [InlineKeyboardButton(d_data["title"], url=d_data["url"])]
      )
    demo_keyboard.append(
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]
    )

    reply_markup = InlineKeyboardMarkup(demo_keyboard)
    await query.message.edit_caption(
        caption=(
            "🎬 **Free Demo Section**\n\nNiche di gayi list se kisi bhi"
            " demo par click karke channel/group join karein:"
        ),
        reply_markup=reply_markup,
    )

  # Back to Home Menu
  elif data == "back_home":
    keyboard = []
    for key, item_data in CONTENT_DATABASE.items():
      keyboard.append([
          InlineKeyboardButton(
              f"{item_data['title']} — {item_data['price']}",
              callback_data=f"buy_{key}",
          )
      ])
    keyboard.append([
        InlineKeyboardButton("🎥 Watch Free Demo", callback_data="demo_menu")
    ])
    keyboard.append(
        [InlineKeyboardButton("💬 Help & Support", url=SUPPORT_TELEGRAM_LINK)]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_caption(
        caption=WELCOME_HEADING, reply_markup=reply_markup
    )

  # Paid Item Purchase Handler
  elif data.startswith("buy_"):
    item_key = data.replace("buy_", "")
    item = CONTENT_DATABASE[item_key]

    payment_text = (
        f"🛍 **{item['title']}**\n"
        f"💰 **Price:** {item['price']}\n\n"
        "1️⃣ **Payment Karein:** Is UPI ID par payment bhejein:\n"
        f"`{UPI_ID}`\n\n"
        "2️⃣ **Screenshot Bhejein:** Payment karne ke baad screenshot is chat"
        " mein bhej dein. Verification ke baad aapko content mil jayega!"
    )
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=payment_text,
        parse_mode="Markdown",
    )


# Main Runner
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
