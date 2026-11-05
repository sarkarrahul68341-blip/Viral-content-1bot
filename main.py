import os
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
UPI_ID = "puja6489@ptyes"  #[span_1](start_span)[span_1](end_span)
SUPPORT_TELEGRAM_LINK = (  # Apna Telegram support username yahan daal sakte hain
    "https://t.me/YourSupportUsername"
)

# --- 2. WELCOME BANNER PHOTO AUR TEXT ---
WELCOME_PHOTO_URL = "https://picsum.photos/800/500"
WELCOME_HEADING = "hello everyone ❤️❤️❤️\n\nWelcome to my official store! Niche diye gaye menu se content choose karein:"

# --- 3. CONTENT & VIDEO/PHOTO LIST ---
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

# --- 4. FREE DEMO CONTENT ---
DEMO_CONTENT = {
    "title": "🎬 Free Demo Content",
    "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
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
      InlineKeyboardButton("🎥 Watch Free Demo", callback_data="show_demo")
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

  if data == "show_demo":
    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=DEMO_CONTENT["media_url"],
        caption=(
            "🎬 Yeh raha aapka Free Demo Content! Agar pasand aaye toh main"
            " menu se purchase karein."
        ),
    )
  elif data.startswith("buy_"):
    item_key = data.replace("buy_", "")
    item = CONTENT_DATABASE[item_key]

    payment_text = (
        f"🛍 **{item['title']}**\n"
        f"💰 **Price:** {item['price']}\n\n"
        "1️⃣ **Payment Karein:** Is UPI ID par payment bhejein:\n"
        f"`{UPI_ID}`\n\n"  #[span_2](start_span)[span_2](end_span)
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
  # Start Flask server in background thread for Render
  t = threading.Thread(target=run_flask)
  t.start()

  # Start Telegram Bot
  app = ApplicationBuilder().token(BOT_TOKEN).build()
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(button_handler))

  print("Business Telegram Bot with Web Server is running...")
  app.run_polling()


if __name__ == "__main__":
  main()
