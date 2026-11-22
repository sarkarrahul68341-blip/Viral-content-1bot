import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN missing hai!")

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
loop = asyncio.new_event_loop()


def _start_loop(target_loop):
    asyncio.set_event_loop(target_loop)
    target_loop.run_forever()


threading.Thread(target=_start_loop, args=(loop,), daemon=True).start()
asyncio.run_coroutine_threadsafe(telegram_app.initialize(), loop).result(timeout=30)


async def start(update: Update, context):
    await update.message.reply_text("Bot live aur start ho gaya hai!")


telegram_app.add_handler(CommandHandler("start", start))

render_url = os.getenv("RENDER_EXTERNAL_URL") or "https://viral-content-1bot-1.onrender.com"
try:
    asyncio.run_coroutine_threadsafe(
        telegram_app.bot.set_webhook(url=f"{render_url.rstrip('/')}/{TELEGRAM_BOT_TOKEN}"), loop
    ).result(timeout=15)
except Exception as e:
    print(f"Webhook error: {e}")


@app.route("/")
def home():
    return "Bot server running!"


@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run_coroutine_threadsafe(telegram_app.process_update(update), loop).result(timeout=30)
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
