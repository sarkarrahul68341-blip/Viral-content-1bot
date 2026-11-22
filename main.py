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
BANNER_PHOTO = os.getenv("BANNER_PHOTO", PACKAGE_PHOTO).strip()

PERMANENT_VIDEOS = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
    10: "",
}

DYNAMIC_STORAGE = {
    "welcome_photo": DEFAULT_PHOTO,
    "banner_photo": BANNER_PHOTO,
}

PACKAGES = {
    "file_1": {"name": "⭐ 01 All mix content VIP Access", "price": 249, "price_badge": "4̶9̶9̶ ➡️ 💎 ₹249", "btn_emoji": "👑", "link": "https://t.me/+s4Zzmwni59diNjU1", "photo": PACKAGE_PHOTO},
    "file_2": {"name": "🔑 02 Rap & Big File VD", "price": 89, "price_badge": "1̶9̶9̶ ➡️ ⚡ ₹89", "btn_emoji": "🎬", "link": "https://t.me/+_AILkUGhVnVkMzBl", "photo": PACKAGE_PHOTO},
    "file_3": {"name": "🔑 03 Mom and Son Real Sex", "price": 45, "price_badge": "9̶9̶ ➡️ 🔥 ₹45", "btn_emoji": "💋", "link": "https://t.me/+qjTxEmHC-z4wMzE1", "photo": PACKAGE_PHOTO},
    "file_4": {"name": "🔞 04 Insta viral reels and sex", "price": 40, "price_badge": "9̶9̶ ➡️ ✨ ₹40", "btn_emoji": "📱", "link": "https://t.me/+LmzeU14SK_I0MGY9", "photo": PACKAGE_PHOTO},
    "file_5": {"name": "🔥 05 Ganga bath group join", "price": 199, "price_badge": "3̶9̶9̶ ➡️ 👑 ₹199", "btn_emoji": "🌊", "link": "https://t.me/+jMs1EZ3RLSc1Yjhl", "photo": PACKAGE_PHOTO},
    "file_6": {"name": "🔥 06 Bath camera hidden", "price": 55, "price_badge": "1̶2̶9̶ ➡️ 💥 ₹55", "btn_emoji": "🎥", "link": "https://t.me/+G4yBWASYMzYzOTc9", "photo": PACKAGE_PHOTO},
    "file_7": {"name": "🔥 07 CP girl real fuke", "price_badge": "1̶4̶9̶ ➡️ 🌟 ₹65", "btn_emoji": "✨", "link": "https://t.me/+f9i3BlsoUeZiZmY1", "photo": PACKAGE_PHOTO},
    "file_8": {"name": "❤️ 08 Sister and brother sex", "price": 30, "price_badge": "7̶9̶ ➡️ 💖 ₹30", "btn_emoji": "❤️", "link": "https://t.me/+BYOIdmg4w3c2MjQ1", "photo": PACKAGE_PHOTO},
}

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
loop = asyncio.new_event_loop()


def _start_loop(target_loop):
    asyncio.set_event_loop(target_loop)
    target_loop.run_forever()


threading.Thread(target=_start_loop, args=(loop,), daemon=True).start()
asyncio.run_coroutine_threadsafe(telegram_app.initialize(), loop).result(timeout=30)


def format_price(pkg):
    return pkg.get("price_badge", f"💎 ₹{pkg['price']}")


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
        [InlineKeyboardButton(f"{pkg['btn_emoji']} {pkg['name']} • {format_price(pkg)} 👉", callback_data=key)]
        for key, pkg in PACKAGES.items()
    ]
    keyboard.append([InlineKeyboardButton("🅵🆁🅴🅴   __   🅳🅴🅼🅾", callback_data="demo_1")])
    keyboard.append([InlineKeyboardButton("💬 Help & Support", url=SUPPORT_LINK)])
    return InlineKeyboardMarkup(keyboard)


async def send_main_menu(context, chat_id):
    caption = (
        "❤️ **Welcome to All Max Content Bot!** ❤️\n\n"
        "🔥 **Special Discount Offer Chal Raha Hai!** "
        "Niche diye gaye packages mein se apna pasandida option select karein:\n"
    )
    photo = DYNAMIC_STORAGE.get("welcome_photo") or (PACKAGE_PHOTO if os.path.exists(PACKAGE_PHOTO) else "")
    return await send_photo_safe(context, chat_id, photo, caption, get_main_menu_keyboard())


async def start(update: Update, context):
    chat_id = update.effective_chat.id
    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.delete()
        except Exception:
            pass
    await send_main_menu(context, chat_id)


async def set_banner_photo(update: Update, context):
    if not update.message or update.effective_user.id != ADMIN_USER_ID:
        return
    if not update.message.photo:
        await update.message.reply_text("⚠️ Banner set karne ke liye photo ke caption mein `/setbanner` likh kar bhejein.")
        return
    banner_file_id = update.message.photo[-1].file_id
    DYNAMIC_STORAGE["banner_photo"] = banner_file_id
    await update.message.reply_text(
        f"✅ **Package Banner Photo update ho gayi!**\n\n`{banner_file_id}`",
        parse_mode="Markdown",
    )


async def handle_photo_or_banner(update: Update, context):
    if not update.message or not update.message.photo:
        return
    caption_text = (update.message.caption or "").strip().lower()
    if "/setbanner" in caption_text or "setbanner" in caption_text:
        await set_banner_photo(update, context)


async def handle_video_id(update: Update, context):
    if not update.message or not update.message.video:
        return
    vid_id = update.message.video.file_id
    await update.message.reply_text(f"🎬 **Video File ID:**\n\n`{vid_id}`", parse_mode="Markdown")


async def callback_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = query.data

    if data == "main_menu":
        try:
            await query.message.delete()
        except Exception:
            pass
        await send_main_menu(context, chat_id)
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
        try:
            await query.message.delete()
        except Exception:
            pass

        video_file_id = PERMANENT_VIDEOS.get(index, "").strip()
        if video_file_id:
            try:
                await context.bot.send_video(
                    chat_id=chat_id, video=video_file_id, caption=text, reply_markup=keyboard, parse_mode="Markdown"
                )
                return
            except BadRequest:
                pass

        fallback_photo = DYNAMIC_STORAGE.get("welcome_photo") or (PACKAGE_PHOTO if os.path.exists(PACKAGE_PHOTO) else "")
        await send_photo_safe(context, chat_id, fallback_photo, text, keyboard)
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        context.user_data["selected_pkg"] = data
        price_str = format_price(pkg)
        banner = (
            DYNAMIC_STORAGE.get("banner_photo")
            or (pkg["photo"] if pkg.get("photo") and os.path.exists(pkg["photo"]) else "")
            or DYNAMIC_STORAGE.get("welcome_photo", "")
        )
        text = (
            f"🖼️✨ **BANNER & PAYMENT** ✨🖼️\n"
            f"💳🔥 **Yahan Pay Karna Hai!** 🔥💳\n"
            f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"📦💎 **Selected Package:** {pkg['name']}\n"
            f"💸💰 **Payable Amount:** **{price_str}** (₹{pkg['price']})\n\n"
            f"👇🔥 **Niche Pay Now button par click karein:** 👇"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💳⚡ Pay Now • {price_str} 🔥🚀", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("🔙🏠 Back to Main Menu", callback_data="main_menu")],
        ])
        try:
            await query.message.delete()
        except Exception:
            pass
        await send_photo_safe(context, chat_id, banner, text, keyboard)
        return

    if data.startswith("pay_"):
        file_key = data.replace("pay_", "")
        pkg = PACKAGES.get(file_key)
        if pkg:
            await query.message.reply_text(
                f"💳⚡ **Pay Now** select ho gaya hai (**{pkg['name']}** — **{format_price(pkg)}**). Agle step mein UPI QR code generate karenge.",
                parse_mode="Markdown",
            )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setbanner", set_banner_photo))
telegram_app.add_handler(CallbackQueryHandler(callback_handler))
telegram_app.add_handler(MessageHandler(filters.VIDEO, handle_video_id))
telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_photo_or_banner))

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
