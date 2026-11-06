import logging
import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
BOT_TOKEN = "9094967544:AAGqnym5ojn1Q9Sm6jIKqoUfWh6-cFxR9rw"
UPI_ID = "puja6489@ptyes"

# Global variable to store current welcome photo file_id dynamically
CURRENT_WELCOME_PHOTO = None

WELCOME_HEADING = (
    "❤️ Welcome to Viral Desi MMS Content Bot ❤️\n\nNiche diye gaye menu se apna"
    " pasandida package ya demo select karein:"
)

# --- FLASK SERVER FOR RENDER KEEP-ALIVE ---
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is active and running 24/7!"


def run_flask():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# --- KEYBOARDS ---
def get_main_menu_keyboard():
  keyboard = [
      [
          InlineKeyboardButton(
              "🔑 01 CP Video and File --------- Rs.249", callback_data="buy_1"
          )
      ],
      [
          InlineKeyboardButton(
              "🔑 02 Rap & CP & Big File VD --------- Rs.89",
              callback_data="buy_2",
          )
      ],
      [
          InlineKeyboardButton(
              "🔑 03 Mom and Son Real Sex --------- Rs.45", callback_data="buy_3"
          )
      ],
      [
          InlineKeyboardButton(
              "🔞 04 Insta viral reels and sex --------- Rs.30",
              callback_data="buy_4",
          )
      ],
      [
          InlineKeyboardButton(
              "🔥 05 Ganga bath group join --------- Rs.199",
              callback_data="buy_5",
          )
      ],
      [
          InlineKeyboardButton(
              "🔥 06 CP Bath camera hidden --------- Rs.55", callback_data="buy_6"
          )
      ],
      [
          InlineKeyboardButton(
              "🔥 07 Pakistani girl real fuke --------- Rs.49",
              callback_data="buy_7",
          )
      ],
      [
          InlineKeyboardButton(
              "❤️ 08 Sister and brother sex --------- Rs.30",
              callback_data="buy_8",
          )
      ],
      [InlineKeyboardButton("🎬 Watch Free Demo", callback_data="open_demos")],
      [InlineKeyboardButton("💬 Help & Support", callback_data="help_support")],
  ]
  return InlineKeyboardMarkup(keyboard)


# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global CURRENT_WELCOME_PHOTO
  reply_markup = get_main_menu_keyboard()

  if CURRENT_WELCOME_PHOTO:
    try:
      await context.bot.send_photo(
          chat_id=update.message.chat_id,
          photo=CURRENT_WELCOME_PHOTO,
          caption=WELCOME_HEADING,
          reply_markup=reply_markup,
          parse_mode="Markdown",
      )
      return
    except Exception as e:
      logger.error(f"Saved photo error: {e}")

  # Fallback to text if no photo is set yet
  await context.bot.send_message(
      chat_id=update.message.chat_id,
      text=WELCOME_HEADING,
      reply_markup=reply_markup,
      parse_mode="Markdown",
  )


async def set_welcome_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global CURRENT_WELCOME_PHOTO

  if not update.message.photo:
    await update.message.reply_text(
        "❌ Kripya kisi photo ke sath `/setphoto` likh kar bhejein!"
    )
    return

  # Get the highest resolution photo file_id
  photo_file_id = update.message.photo[-1].file_id
  CURRENT_WELCOME_PHOTO = photo_file_id

  await update.message.reply_text(
      "✅ **Success!** Naya welcome photo successfully set ho gaya hai.\nAb koi"
      " bhi `/start` karega toh yeh photo dikhegi."
  )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  data = query.data

  if data.startswith("buy_"):
    package_id = data.split("_")[1]
    prices = {
        "1": "Rs.249",
        "2": "Rs.89",
        "3": "Rs.45",
        "4": "Rs.30",
        "5": "Rs.199",
        "6": "Rs.55",
        "7": "Rs.49",
        "8": "Rs.30",
    }
    price = prices.get(package_id, "Rs.0")

    text = (
        f"✨ **Package {package_id} Selected** ✨\n\nPrice: **{price}**\n\nPayment"
        f" karne ke liye niche diye gaye UPI ID par payment karein:\n📌 UPI ID:"
        f" `{UPI_ID}`\n\nPayment karne ke baad screenshot ya UTR number yahan"
        " bhej dein taaki aapko content turant mil sake!"
    )
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data="back_home")]]
    try:
      await query.edit_message_caption(
          caption=text,
          reply_markup=InlineKeyboardMarkup(keyboard),
          parse_mode="Markdown",
      )
    except:
      await query.edit_message_text(
          text=text,
          reply_markup=InlineKeyboardMarkup(keyboard),
          parse_mode="Markdown",
      )

  elif data == "open_demos":
    text = (
        "🎬 **Free Demos:**\nAap hamare free demos yahan dekh sakte"
        " hain:\n👉 [Click Here for Demo Channel](https://t.me/your_demo_channel)"
    )
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data="back_home")]]
    try:
      await query.edit_message_caption(
          caption=text,
          reply_markup=InlineKeyboardMarkup(keyboard),
          parse_mode="Markdown",
      )
    except:
      await query.edit_message_text(
          text=text,
          reply_markup=InlineKeyboardMarkup(keyboard),
          parse_mode="Markdown",
      )

  elif data == "help_support":
    text = (
        "💬 **Help & Support**\n\nAgar aapko payment ya content access karne"
        " mein koi bhi problem aa rahi hai, toh aap seedhe admin se contact"
        " kar sakte hain:\n👉 Admin: @your_admin_username"
    )
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data="back_home")]]
    try:
      await query.edit_message_caption(
          caption=text,
          reply_markup=InlineKeyboardMarkup(keyboard),
          parse_mode="Markdown",
      )
    except:
      await query.edit_message_text(
          text=text,
          reply_markup=InlineKeyboardMarkup(keyboard),
          parse_mode="Markdown",
      )

  elif data == "back_home":
    global CURRENT_WELCOME_PHOTO
    reply_markup = get_main_menu_keyboard()
    if CURRENT_WELCOME_PHOTO:
      try:
        await query.message.delete()
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=CURRENT_WELCOME_PHOTO,
            caption=WELCOME_HEADING,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        return
      except:
        pass

    try:
      await query.edit_message_caption(
          caption=WELCOME_HEADING,
          reply_markup=reply_markup,
          parse_mode="Markdown",
      )
    except:
      await query.edit_message_text(
          text=WELCOME_HEADING,
          reply_markup=reply_markup,
          parse_mode="Markdown",
      )


def main():
  t = threading.Thread(target=run_flask)
  t.daemon = True
  t.start()

  application = ApplicationBuilder().token(BOT_TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("setphoto", set_welcome_photo))
  application.add_handler(CallbackQueryHandler(button_handler))

  logger.info("Bot is starting...")
  application.run_polling()


if __name__ == "__main__":
  main()
    
