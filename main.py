import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN missing hai! Render Environment mein token set karein.")

SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "8776203848"))
PERMANENT_CHANNEL_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
PERMANENT_BUTTON_NAME = "Join Demo 2"
DEFAULT_PHOTO = os.getenv("DEFAULT_PHOTO", "").strip()
PACKAGE_PHOTO = "VIP New.jpg"

PERMANENT_VIDEOS = {
    1: "BAACAgUAAxkBAAIF1mr9OhyTVF2iSYJ4zZYxjH5AqKdYAAK1IQAC08jpV-yeriahxLGXPQQ",
    2: "BAACAgUAAxkBAAIF2Gr9Oj41G_dAdis5uciBnfjUWRWRAAK3IQAC08jpVyGIegbxq4mgPQQ",
    3: "BAACAgUAAxkBAAIF3Gr9P-LP6eT8P8RCe1BOa3oOMRdIAALEIQAC08jpV5UMTjGj4ED1PQQ",
    4: "BAACAgUAAxkBAAIF82r9QqQR0P0JXC8lgC9ZJWcdhfa7AALRIQAC08jpVwuR50arGNMuPQQ",
    5: "BAACAgUAAxkBAAIF9Wr9QroENszvSIbGapfoYUM6IeE1AALSIQAC08jpV0Inq7sUJmp0PQQ",
    6: "BAACAgUAAxkBAAIF2mr9OlpY8-8Lba01XQKIkxt22V8gAAK4IQAC08jpV-WIhsT1ykHjPQQ",
    7: "BAACAgUAAxkBAAIGKWr9Sdwq1TIWMRxNKTij6xxpVwWDAAL1IQAC08jpV2_6CG9awMplPQQ",
    8: "BAACAgUAAxkBAAIGK2r9SimPlWBIXnA5-vOjgovjnwnVAAL4IQAC08jpV7WJKbV5SZk5PQQ",
    9: "BAACAgUAAxkBAAIGMWr9SnaiUrhdJaPsyZciIbsiLzdiAAL5IQAC08jpVyy-uKqA2eLmPQQ",
    10: "BAACAgUAAxkBAAIKV2r-m91Iw9Nsgl2fAAHdeSDg_YlC6gACzSEAAoct-VfaqbAts5Yu-T0E",
}

DYNAMIC_STORAGE = {"welcome_photo": DEFAULT_PHOTO}

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


async def delete_tracked_bot_messages(context, chat_id, exclude_msg_id=None):
    msg_ids = context.user_data.pop("bot_msg_ids", [])
    kept_ids = []
    for mid in msg_ids:
        if exclude_msg_id and mid == exclude_msg_id:
            kept_ids.append(mid)
            continue
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=mid)
        except Exception:
            pass
    context.user_data["bot_msg_ids"] = kept_ids


def remember_bot_message(context, message_id):
    if not message_id:
        return
    msg_ids = context.user_data.setdefault("bot_msg_ids", [])
    if message_id not in msg_ids:
        msg_ids.append(message_id)
    if len(msg_ids) > 15:
        context.user_data["bot_msg_ids"] = msg_ids[-15:]


async def clear_previous_view(context, chat_id, query_message=None):
    exclude_id = query_message.message_id if query_message else None
    if query_message:
        try:
            await query_message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
    await delete_tracked_bot_messages(context, chat_id, exclude_msg_id=exclude_id)
    if query_message:
        try:
            await query_message.delete()
        except Exception:
            pass


async def send_photo_safe(context, chat_id, photo, caption, reply_markup):
    if photo:
        try:
            if os.path.exists(photo):
                with open(photo, "rb") as f:
                    return await context.bot.send_photo(
                        chat_id=chat_id, photo=f, caption=caption, reply_markup=reply_markup, parse_mode="Markdown"
                    )
            return await context.bot.send_photo(
                chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode="Markdown"
            )
        except BadRequest as e:
            print(f"Photo fallback to text: {e}")
    return await context.bot.send_message(
        chat_id=chat_id, text=caption, reply_markup=reply_markup, parse_mode="Markdown"
    )


def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(f"{pkg['btn_emoji']} {pkg['name']} • {pkg['price_badge']} 👉", callback_data=key)]
        for key, pkg in PACKAGES.items()
    ]
    keyboard.append([InlineKeyboardButton("🅵🆁🅴🅴   __   🅳🅴🅼🅾", callback_data="demo_1")])
    keyboard.append([InlineKeyboardButton("💬 Help & Support", url=SUPPORT_LINK)])
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context):
    caption = (
        "❤️ **Welcome to All Max Content Bot!** ❤️\n\n"
        "🔥 **Special Discount Offer Chal Raha Hai!** "
        "Niche diye gaye packages mein se apna pasandida option select karein:\n"
    )
    photo = DYNAMIC_STORAGE.get("welcome_photo") or (PACKAGE_PHOTO if os.path.exists(PACKAGE_PHOTO) else "")
    if update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat_id
        await clear_previous_view(context, chat_id, query.message)
        sent = await send_photo_safe(context, chat_id, photo, caption, get_main_menu_keyboard())
        remember_bot_message(context, sent.message_id)
    else:
        chat_id = update.effective_chat.id
        await clear_previous_view(context, chat_id)
        sent = await send_photo_safe(context, chat_id, photo, caption, get_main_menu_keyboard())
        remember_bot_message(context, sent.message_id)


async def handle_admin_video(update: Update, context):
    if not update.message or not update.message.video or update.effective_user.id != ADMIN_USER_ID:
        return
    video_file_id = update.message.video.file_id
    PERMANENT_VIDEOS[10] = video_file_id
    await update.message.reply_text(f"✅ **Demo 10 video update ho gayi!**\n\n`{video_file_id}`", parse_mode="Markdown")


async def callback_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = query.data

    if data == "main_menu":
        await start(update, context)
        return

    if data.startswith("demo_"):
        try:
            index = int(data.replace("demo_", ""))
        except ValueError:
            index = 1
        index = max(1, min(10, index))

        nav_buttons = []
        row = []
        if index > 1:
            row.append(InlineKeyboardButton("⬅️ 🎬 Prev Clip", callback_data=f"demo_{index - 1}"))
        if index < 10:
            row.append(InlineKeyboardButton("Next Clip 🎬 ➡️", callback_data=f"demo_{index + 1}"))
        if row:
            nav_buttons.append(row)
        if index == 10:
            nav_buttons.append([InlineKeyboardButton("🔥👑 Get Full VIP Access • 4̶9̶9̶ ➡️ 💎 ₹249 🚀", callback_data="file_1")])
        nav_buttons.append([InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")])
        nav_buttons.append([InlineKeyboardButton(PERMANENT_BUTTON_NAME, url=PERMANENT_CHANNEL_LINK)])
        keyboard = InlineKeyboardMarkup(nav_buttons)

        text = f"🎬 **Demo Clip {index} / 10**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n✨ Yeh hamari demo clip number {index} hai."
        await clear_previous_view(context, chat_id, query.message)

        video_file_id = PERMANENT_VIDEOS.get(index)
        if video_file_id:
            try:
                sent = await context.bot.send_video(
                    chat_id=chat_id, video=video_file_id, caption=text, reply_markup=keyboard, parse_mode="Markdown"
                )
            except BadRequest:
                sent = await context.bot.send_message(
                    chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode="Markdown"
                )
        else:
            fallback_photo = DYNAMIC_STORAGE.get("welcome_photo") or (PACKAGE_PHOTO if os.path.exists(PACKAGE_PHOTO) else "")
            sent = await send_photo_safe(context, chat_id, fallback_photo, text, keyboard)
        remember_bot_message(context, sent.message_id)
        return

    pkg = PACKAGES.get(data)
    if pkg:
        await query.message.reply_text(
            f"📦 **{pkg['name']}**\n💸 **Offer Price:** {pkg['price_badge']}\n\nDemo feature ready hai! Agle step mein Pay Now aur QR payment add karenge.",
            parse_mode="Markdown"
        )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(callback_handler))
telegram_app.add_handler(MessageHandler(filters.VIDEO, handle_admin_video))

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
                
