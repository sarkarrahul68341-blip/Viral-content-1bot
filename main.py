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
BOT_TOKEN = "9094967544:AAF5DabOpMI3x88twq0Kl3rWl-0MBl94vVs"
UPI_ID = "puja6489@ptyes"
MERCHANT_NAME = "Viral Desi Content"

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
              "🔑 01 CP Video and File --------- Rs.249", callback_data="pkg_1"
          )
      ],
      [
          InlineKeyboardButton(
              "🔑 02 Rap & CP & Big File VD --------- Rs.89",
              callback_data="pkg_2",
          )
      ],
      [
          InlineKeyboardButton(
              "🔑 03 Mom and Son Real Sex --------- Rs.45", callback_data="pkg_3"
          )
      ],
      [
          InlineKeyboardButton(
              "🔞 04 Insta viral reels and sex --------- Rs.30",
              callback_data="pkg_4",
          )
      ],
      [
          InlineKeyboardButton(
              "🔥 05 Ganga bath group join --------- Rs.199",
              callback_data="pkg_5",
          )
      ],
      [
          InlineKeyboardButton(
              "🔥 06 CP Bath camera hidden --------- Rs.55",
              callback_data="pkg_6",
          )
      ],
      [
          InlineKeyboardButton(
              "🔥 07 Pakistani girl real fuke --------- Rs.49",
              callback_data="pkg_7",
          )
      ],
      [
          InlineKeyboardButton(
              "❤️ 08 Sister and brother sex --------- Rs.30",
              callback_data="pkg_8",
          )
      ],
      [InlineKeyboardButton("🎬 Watch Free Demo", callback_data="demo_menu")],
      [InlineKeyboardButton("💬 Help & Support", callback_data="help_menu")],
  ]
  return InlineKeyboardMarkup(keyboard)


# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global CURRENT_WELCOME_PHOTO
  reply_markup = get_main_menu_keyboard()
  chat_id = update.message.chat_id

  if CURRENT_WELCOME_PHOTO:
    try:
      await context.bot.send_photo(
          chat_id=chat_id,
          photo=CURRENT_WELCOME_PHOTO,
          caption=WELCOME_HEADING,
          reply_markup=reply_markup,
      )
      return
    except Exception as e:
      logger.error(f"Welcome photo error: {e}")

  await context.bot.send_message(
      chat_id=chat_id, text=WELCOME_HEADING, reply_markup=reply_markup
  )


async def set_welcome_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global CURRENT_WELCOME_PHOTO
  if not update.message.photo:
    await update.message.reply_text(
        "❌ Kripya kisi photo ke sath `/setphoto` likh kar bhejein!"
    )
    return

  CURRENT_WELCOME_PHOTO = update.message.photo[-1].file_id
  await update.message.reply_text(
      "✅ Success! Naya welcome photo successfully set ho gaya hai."
  )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  data = query.data
  chat_id = query.message.chat_id

  # Har package ke alag-alag amounts aur display prices
  prices_num = {
      "1": "249.00",
      "2": "89.00",
      "3": "45.00",
      "4": "30.00",
      "5": "199.00",
      "6": "55.00",
      "7": "49.00",
      "8": "30.00",
  }
  price_display = {
      "1": "Rs.249",
      "2": "Rs.89",
      "3": "Rs.45",
      "4": "Rs.30",
      "5": "Rs.199",
      "6": "Rs.55",
      "7": "Rs.49",
      "8": "Rs.30",
  }

  if data == "main_menu":
    try:
      await query.message.delete()
    except:
      pass
    reply_markup = get_main_menu_keyboard()
    if CURRENT_WELCOME_PHOTO:
      try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=CURRENT_WELCOME_PHOTO,
            caption=WELCOME_HEADING,
            reply_markup=reply_markup,
        )
        return
      except:
        pass
    await context.bot.send_message(
        chat_id=chat_id, text=WELCOME_HEADING, reply_markup=reply_markup
    )
    return

  if data.startswith("pkg_"):
    pkg_id = data.split("_")[1]
    amount = prices_num.get(pkg_id, "30.00")
    price_text = price_display.get(pkg_id, "Rs.30")

    # Har package ke hisab se exact amount wali UPI link
    upi_url = (
        f"upi://pay?pa={UPI_ID}&pn={MERCHANT_NAME}&am={amount}&cu=INR&tn=Package"
        f" {pkg_id}"
    )

    text = (
        f"✨ Package {pkg_id} Selected ✨\n\nPrice: {price_text}\n\nPayment"
        " karne ke liye niche diye gaye 'Pay Now' button par click"
        f" karein:\n📌 UPI ID: {UPI_ID}\n\nPayment karne ke baad screenshot ya"
        " UTR number yahan bhej dein taaki content turant mil sake!"
    )

    keyboard = [
        [InlineKeyboardButton(f"💳 Pay {price_text} Now", url=upi_url)],
        [InlineKeyboardButton("« Back to Menu", callback_data="main_menu")],
    ]

  elif data == "demo_menu":
    text = (
        "🎬 Free Demos:\nAap hamare free demos yahan dekh sakte"
        " hain:\n👉 Click Here for Demo Channel: https://t.me/your_demo_channel"
    )
    keyboard = [
        [InlineKeyboardButton("« Back to Menu", callback_data="main_menu")]
    ]

  elif data == "help_menu":
    text = (
        "💬 Help & Support\n\nAgar aapko payment ya content access karne mein"
        " koi bhi problem aa rahi hai, toh aap seedhe admin se contact kar"
        " sakte hain:\n👉 Admin: @your_admin_username"
    )
    keyboard = [
        [InlineKeyboardButton("« Back to Menu", callback_data="main_menu")]
    ]
  else:
    return

  try:
    await query.message.delete()
  except:
    pass

  await context.bot.send_message(
      chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard)
  )


def main():
  t = threading.Thread(target=run_flask)
  t.daemon = True
  t.start()

  application = ApplicationBuilder().token(BOT_TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("setphoto", set_welcome_photo))
  application.add_handler(
      MessageHandler(filters.PHOTO & ~filters.Command(), set_welcome_photo)
  )
  application.add_handler(CallbackQueryHandler(button_handler))

  logger.info("Bot is starting...")
  application.run_polling()


if __name__ == "__main__":
  main()
