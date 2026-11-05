from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# --- 1. APNI DETAILS YAHAN SET KAREIN ---
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_FROM_BOTFATHER"
UPI_ID = "yourname@paytm"  # Apni UPI ID dalein
SUPPORT_TELEGRAM_LINK = "https://t.me/YourSupportUsername"  # Apna Telegram support link dalein

# --- 2. WELCOME BANNER PHOTO AUR TEXT ---
WELCOME_PHOTO_URL = "https://picsum.photos/800/500"  # Yahan apni banner photo ka direct link dalein
WELCOME_HEADING = "hello everyone ❤️❤️❤️\n\nWelcome to my official store! Niche diye gaye menu se content choose karein:"

# --- 3. CONTENT & VIDEO/PHOTO LIST (Aap yahan sab kuch edit kar sakte hain) ---
CONTENT_DATABASE = {
    "item_1": {
        "title": "🔥 Premium Video Package 1",
        "price": "₹199",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",  # Video Link
        "type": "video",
    },
    "item_2": {
        "title": "💎 Exclusive Photo Collection",
        "price": "₹99",
        "media_url": "https://picsum.photos/600/400",  # Photo Link
        "type": "photo",
    },
}

# --- 4. FREE DEMO CONTENT ---
DEMO_CONTENT = {
    "title": "🎬 Free Demo Content",
    "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
}


# Start Command (Fast Welcome Message + Photo Banner + Menu List)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # Dynamic Menu Buttons tayar karna
  keyboard = []

  # Content List Buttons
  for key, data in CONTENT_DATABASE.items():
    keyboard.append([
        InlineKeyboardButton(
            f"{data['title']} — {data['price']}", callback_data=f"buy_{key}"
        )
    ])

  # Demo Button
  keyboard.append([
      InlineKeyboardButton("🎥 Watch Free Demo", callback_data="show_demo")
  ])

  # Help & Support Button (Telegram Link)
  keyboard.append(
      [InlineKeyboardButton("💬 Help & Support", url=SUPPORT_TELEGRAM_LINK)]
  )

  reply_markup = InlineKeyboardMarkup(keyboard)

  # Sabse pehle Photo bhejenge, aur photo ke niche welcome text aur buttons rahenge
  await context.bot.send_photo(
      chat_id=update.message.chat_id,
      photo=WELCOME_PHOTO_URL,
      caption=WELCOME_HEADING,
      reply_markup=reply_markup,
  )


# Button Click Handler (Video, Photo, Demo, Payment)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  data = query.data

  # Agar user ne Demo manga
  if data == "show_demo":
    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=DEMO_CONTENT["media_url"],
        caption=(
            "🎬 Yeh raha aapka Free Demo Content! Agar pasand aaye toh main"
            " menu se purchase karein."
        ),
    )

  # Agar user ne koi paid item select kiya (Payment & UPI)
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
if __name__ == "__main__":
  app = ApplicationBuilder().token(BOT_TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(button_handler))

  print("Business Telegram Bot with Photo Banner is running...")
  app.run_polling()
