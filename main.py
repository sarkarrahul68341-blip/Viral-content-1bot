import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN missing hai! Render Environment mein token set karein.")

SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
DEFAULT_PHOTO = os.getenv("DEFAULT_PHOTO", "").strip()
PACKAGE_PHOTO = "VIP New.jpg"

PACKAGES = {
    "file_1": {"name": "⭐ 01 All mix content VIP Access", "price_badge": "4̶9̶9̶ ➡️ 💎 ₹249", "btn_emoji": "👑"},
    "file_2": {"name": "🔑 02 Rap & Big File VD", "price_badge": "1̶9̶9̶ ➡️ ⚡ ₹89", "btn_emoji": "🎬"},
    "file_3": {"name": "🔑 03 Mom and Son Real Sex", "price_badge": "9̶9̶ ➡️ 🔥 ₹45", "btn_emoji": "💋"},
    "file_4": {"name": "🔞 04 Insta viral reels and sex", "price_badge": "9̶9̶ ➡️ ✨ ₹40", "btn_emoji": "📱"},
    "file_5": {"name": "🔥 05 Ganga bath group join", "price_badge": "3̶9̶9̶ ➡️ 👑 ₹199", "btn_emoji": "🌊"},
    "file_6": {"name": "🔥 06 Bath camera hidden", "price_badge": "1̶2̶9̶ ➡️ 💥 ₹55", "btn_emoji": "🎥"},
    "file_7": {"name": "🔥 07 CP girl real fuke", "price_badge": "1̶4̶9̶ ➡️ 🌟 ₹65", "btn_emoji": "✨"},
    "file_8": {"name": "❤️ 08 Sister and brother sex", "price_badge": "7̶9̶ ➡️ 💖 ₹30", "btn_emoji": "❤️"},
}

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
loop = asyncio.new_event_loop()


def _start_loop(target_loop):
    asyncio.set_event_loop(target_loop)
    target_loop.run_forever()


threading.Thread(target=_start_loop, args=(loop,), daemon=True).start()
asyncio.run_coroutine_threadsafe(telegram_app.initialize(), loop).result(timeout=30)


def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(f"{pkg['btn_emoji']} {pkg['name']} • {pkg['price_badge']} 👉", callback_data=key)]
        for key, pkg in PACKAGES.items()
    ]
    keyboard.append([InlineKeyboardButton("🅵🆁🅴🅴   __   🅳🅴🅼🅾", callback_data="demo_1")])
    keyboard.append([InlineKeyboardButton("💬 Help & Support", url=SUPPORT_LINK)])
    return InlineKeyboardMarkup(keyboard)


async def send_menu(context, chat_id):
    caption = (
        "❤️ **Welcome to All Max Content Bot!** ❤️\n\n"
        "🔥 **Special Discount Offer Chal Raha Hai!** "
        "Niche diye gaye packages mein se apna pasandida option select karein:\n"
    )
    markup = get_main_menu_keyboard()
    photo = DEFAULT_PHOTO or (PACKAGE_PHOTO if os.path.exists(PACKAGE_PHOTO) else "")

    if photo:
        try:
            if os.path.exists(photo):
                with open(photo, "rb") as f:
                    return await context.bot.send_photo(
                        chat_id=chat_id, photo=f, caption=caption, reply_markup=markup, parse_mode="Markdown"
                    )
            return await context.bot.send_photo(
                chat_id=chat_id, photo=photo, caption=caption, reply_markup=markup, parse_mode="Markdown"
            )
        except BadRequest:
            pass

    return await context.bot.send_message(
        chat_id=chat_id, text=caption, reply_markup=markup, parse_mode="Markdown"
    )


async def start(update: Update, context):
    chat_id = update.effective_chat.id
    await send_menu(context, chat_id)


async def menu_callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    pkg = PACKAGES.get(query.data)
    if pkg:
        await query.message.reply_text(
            f"📦 **{pkg['name']}**\n💸 **Offer Price:** {pkg['price_badge']}\n\nMenu panel ka test safal raha! Aage Pay Now aur screenshot flow add kiya jayega.",
            parse_mode="Markdown"
        )
    elif query.data == "demo_1":
        await query.message.reply_text("🎬 **Free Demo** button ka test safal raha!")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(menu_callback))

render_url = os.getenv("RENDER_EXTERNAL_URL") or "https://viral-content-1bot-1.onrender.com"
try:
    asyncio.run_coroutine_threadsafe(
        telegram_app.bot.set_webhook(url=f"{render_url.rstrip('/')}/{TELEGRAM_BOT_TOKEN}"), loop
    ).result(timeout=15)
except Exception as e:
    print(f"Webhook setup error: {e}")


@app.route("/")
def home():
    return "Bot Webhook Server is Running!"


@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run_coroutine_threadsafe(telegram_app.process_update(update), loop).result(timeout=30)
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
