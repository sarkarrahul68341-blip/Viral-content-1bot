import os
import time
import asyncio
import threading
import urllib.parse
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
UPI_ID = os.getenv("UPI_ID", "Puja6489@ptyes")
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "All Max Content Bot")
SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
ADMIN_USER_ID = 8776203848
PERMANENT_CHANNEL_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
PERMANENT_BUTTON_NAME = "Join Demo 2"
DEFAULT_PHOTO = "AgACAgUAAxkBAAIKmWr-ocEknsMPFV0Ua2SDhjUpjx8SAAKzEmsbhy35V-O7-QS5ebgsAQADAgADeAADPQQ"
PACKAGE_PHOTO = "VIP New.jpg"
SCREENSHOT_VALIDITY_SECONDS = 24 * 60 * 60
USED_SCREENSHOTS = {}

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
    "file_1": {"name": "⭐ 01 All mix content VIP Access", "price": 249, "price_badge": "4̶9̶9̶ ➡️ 💎 ₹249", "btn_emoji": "👑", "link": "https://t.me/+s4Zzmwni59diNjU1", "photo": PACKAGE_PHOTO},
    "file_2": {"name": "🔑 02 Rap & Big File VD", "price": 89, "price_badge": "1̶9̶9̶ ➡️ ⚡ ₹89", "btn_emoji": "🎬", "link": "https://t.me/+_AILkUGhVnVkMzBl", "photo": PACKAGE_PHOTO},
    "file_3": {"name": "🔑 03 Mom and Son Real Sex", "price": 45, "price_badge": "9̶9̶ ➡️ 🔥 ₹45", "btn_emoji": "💋", "link": "https://t.me/+qjTxEmHC-z4wMzE1", "photo": PACKAGE_PHOTO},
    "file_4": {"name": "🔞 04 Insta viral reels and sex", "price": 40, "price_badge": "9̶9̶ ➡️ ✨ ₹40", "btn_emoji": "📱", "link": "https://t.me/+LmzeU14SK_I0MGY9", "photo": PACKAGE_PHOTO},
    "file_5": {"name": "🔥 05 Ganga bath group join", "price": 199, "price_badge": "3̶9̶9̶ ➡️ 👑 ₹199", "btn_emoji": "🌊", "link": "https://t.me/+jMs1EZ3RLSc1Yjhl", "photo": PACKAGE_PHOTO},
    "file_6": {"name": "🔥 06 Bath camera hidden", "price": 55, "price_badge": "1̶2̶9̶ ➡️ 💥 ₹55", "btn_emoji": "🎥", "link": "https://t.me/+G4yBWASYMzYzOTc9", "photo": PACKAGE_PHOTO},
    "file_7": {"name": "🔥 07 CP girl real fuke", "price": 65, "price_badge": "1̶4̶9̶ ➡️ 🌟 ₹65", "btn_emoji": "✨", "link": "https://t.me/+f9i3BlsoUeZiZmY1", "photo": PACKAGE_PHOTO},
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


def is_screenshot_already_used_today(file_unique_id):
    now = time.time()
    for k in [k for k, ts in USED_SCREENSHOTS.items() if (now - ts) >= SCREENSHOT_VALIDITY_SECONDS]:
        del USED_SCREENSHOTS[k]
    if file_unique_id in USED_SCREENSHOTS:
        return True
    USED_SCREENSHOTS[file_unique_id] = now
    return False


def is_expired_or_old_screenshot(message):
    if not message:
        return False
    if getattr(message, "forward_date", None) or getattr(message, "forward_origin", None):
        return True
    if getattr(message, "date", None):
        age_seconds = time.time() - message.date.timestamp()
        if age_seconds > SCREENSHOT_VALIDITY_SECONDS:
            return True
    return False


async def cleanup_previous_user_screenshots(context, chat_id, new_msg_id):
    old_ids = context.user_data.pop("user_screenshot_ids", [])
    for mid in old_ids:
        if mid != new_msg_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=mid)
            except Exception:
                pass
    context.user_data["user_screenshot_ids"] = [new_msg_id] if new_msg_id else []


async def replace_bot_message(context, chat_id, query_message=None):
    ids_to_delete = set()
    last_id = context.user_data.pop("last_bot_msg_id", None)
    if last_id:
        ids_to_delete.add(last_id)
    for mid in context.user_data.pop("bot_msg_ids", []):
        ids_to_delete.add(mid)
    if query_message and query_message.message_id:
        ids_to_delete.add(query_message.message_id)

    for mid in ids_to_delete:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=mid)
        except Exception:
            pass


def set_single_bot_message(context, message_id):
    if message_id:
        context.user_data["last_bot_msg_id"] = message_id
        context.user_data["bot_msg_ids"] = [message_id]


def generate_upi_qr(amount, order_id):
    encoded_name = urllib.parse.quote(BUSINESS_NAME)
    encoded_note = urllib.parse.quote(f"Order_{order_id}")
    upi_uri = f"upi://pay?pa={UPI_ID}&pn={encoded_name}&am={amount}&cu=INR&tn={encoded_note}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"qr_{order_id}.png"
    img.save(filename)
    return filename


def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(f"{pkg['btn_emoji']} {pkg['name']} • {format_price(pkg)} 👉", callback_data=key)]
        for key, pkg in PACKAGES.items()
    ]
    keyboard.append([InlineKeyboardButton("🅵🆁🅴🅴   __   🅳🅴🅼🅾", callback_data="demo_1")])
    keyboard.append([InlineKeyboardButton("💬 Help & Support", url=SUPPORT_LINK)])
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context):
    caption = "❤️ **Welcome to All Max Content Bot!** ❤️\n\n🔥 **Special Discount Offer Chal Raha Hai!** Niche diye gaye packages mein se apna pasandida option select karein:\n"
    photo = DYNAMIC_STORAGE.get("welcome_photo", DEFAULT_PHOTO)
    if update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat_id
        await replace_bot_message(context, chat_id, query.message)
        sent = await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
        set_single_bot_message(context, sent.message_id)
    else:
        chat_id = update.effective_chat.id
        await replace_bot_message(context, chat_id)
        sent = await update.message.reply_photo(photo=photo, caption=caption, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
        set_single_bot_message(context, sent.message_id)


async def process_photo_setting(update: Update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("⛔ Sirf admin hi photo update kar sakta hai.")
        return
    if not update.message.photo:
        await update.message.reply_text("⚠️ Kripya photo ke sath `/setphoto` likhein.")
        return
    photo_file = update.message.photo[-1].file_id
    DYNAMIC_STORAGE["welcome_photo"] = photo_file
    await update.message.reply_text(f"✅ **Welcome photo update ho gayi!**\n\n`{photo_file}`", parse_mode="Markdown")


async def handle_admin_video(update: Update, context):
    if not update.message or not update.message.video or update.effective_user.id != ADMIN_USER_ID:
        return
    video_file_id = update.message.video.file_id
    PERMANENT_VIDEOS[10] = video_file_id
    await update.message.reply_text(f"✅ **Demo 10 video update ho gayi!**\n\n`{video_file_id}`", parse_mode="Markdown")


async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    chat_id = query.message.chat_id
    data = query.data

    if data == "main_menu":
        await start(update, context)
        return

    if data.startswith("approve_") or data.startswith("reject_"):
        if user_id != ADMIN_USER_ID:
            await query.answer("⛔ Sirf admin hi approve ya reject kar sakta hai.", show_alert=True)
            return
        parts = data.split("_", 2)
        if len(parts) == 3:
            action, target_user_str, file_key = parts
            target_user_id = int(target_user_str)
            pkg = PACKAGES.get(file_key, PACKAGES["file_1"])
            price_str = format_price(pkg)
            if action == "approve":
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"✅ **Payment Approved!**\n\n📦 **Package:** {pkg['name']}\n💸 **Offer Price:** **{price_str}**\n✨ Niche diye gaye button se apna VIP Access link kholen:",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔗 🔓 Access VIP Content Link 🚀", url=pkg["link"])],
                        [InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]
                    ]),
                    parse_mode="Markdown"
                )
                try:
                    await query.edit_message_caption(caption=(query.message.caption or "") + "\n\n✅ **APPROVED**", parse_mode="Markdown")
                except Exception:
                    pass
            else:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"❌ **Payment Rejected!**\n\n📦 **Package:** {pkg['name']}\n💸 **Offer Price:** **{price_str}**\n⚠️ Aapka payment screenshot valid nahi tha. Aap dobara package select karke QR generate kar sakte hain.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]]),
                    parse_mode="Markdown"
                )
                try:
                    await query.message.delete()
                except Exception:
                    pass
        return

    if data.startswith("demo_"):
        try:
            index = int(data.replace("demo_", ""))
        except ValueError:
            index = 1
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
        await replace_bot_message(context, chat_id, query.message)
        video_file_id = PERMANENT_VIDEOS.get(index)
        if video_file_id:
            sent = await context.bot.send_video(chat_id=chat_id, video=video_file_id, caption=text, reply_markup=keyboard, parse_mode="Markdown")
        else:
            sent = await context.bot.send_photo(chat_id=chat_id, photo=DYNAMIC_STORAGE.get("welcome_photo", DEFAULT_PHOTO), caption=text, reply_markup=keyboard, parse_mode="Markdown")
        set_single_bot_message(context, sent.message_id)
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        context.user_data["selected_pkg"] = data
        price_str = format_price(pkg)
        text = f"🔥💎 **SELECTED VIP PACKAGE** 💎🔥\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n📦 **Package:** {pkg['name']}\n💸 **Offer Price:** **{price_str}**\n\n✨ **Payment karne ke liye niche diye gaye button par click karein:** 👇"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💳 ⚡ Pay Now • {price_str} 🔥", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]
        ])
        await replace_bot_message(context, chat_id, query.message)
        if pkg["photo"] and os.path.exists(pkg["photo"]):
            with open(pkg["photo"], "rb") as photo_file:
                sent = await context.bot.send_photo(chat_id=chat_id, photo=photo_file, caption=text, reply_markup=keyboard, parse_mode="Markdown")
        else:
            sent = await context.bot.send_photo(chat_id=chat_id, photo=DEFAULT_PHOTO, caption=text, reply_markup=keyboard, parse_mode="Markdown")
        set_single_bot_message(context, sent.message_id)
        return

    if data.startswith("pay_"):
        file_key = data.replace("pay_", "")
        pkg = PACKAGES.get(file_key)
        if not pkg:
            return
        context.user_data["selected_pkg"] = file_key
        context.user_data["qr_generated_for"] = file_key
        qr_file_path = None
        price_str = format_price(pkg)
        try:
            qr_file_path = generate_upi_qr(pkg["price"], user_id)
            caption = f"🚨📱 **SCAN & PAY INSTRUCTIONS** 📱🚨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n📦 **Package:** {pkg['name']}\n💸 **Amount to Pay:** **{price_str}**\n\n1️⃣ Is QR Code ko scan karke **₹{pkg['price']}** pay karein (`{UPI_ID}`).\n2️⃣ Payment karne ke baad is chat mein **Payment ka Screenshot** bhejien. Approve hone ke baad link milega."
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]])
            await replace_bot_message(context, chat_id, query.message)
            with open(qr_file_path, "rb") as photo:
                sent = await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown")
            set_single_bot_message(context, sent.message_id)
        finally:
            if qr_file_path and os.path.exists(qr_file_path):
                try:
                    os.remove(qr_file_path)
                except Exception:
                    pass


async def handle_media(update: Update, context):
    if not update.message.photo:
        return
    if "setphoto" in (update.message.caption or "").lower():
        await process_photo_setting(update, context)
        return

    chat_id = update.effective_chat.id
    photo_obj = update.message.photo[-1]
    await cleanup_previous_user_screenshots(context, chat_id, update.message.message_id)

    qr_pkg_key = context.user_data.get("qr_generated_for")
    if not qr_pkg_key or qr_pkg_key not in PACKAGES:
        await replace_bot_message(context, chat_id)
        sent = await update.message.reply_text(
            "❌ **Payment Rejected!**\n\nSirf payment ka screenshot hi bhej sakte hain. Kripya pehle package select karke Pay Now se payment karein.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]),
            parse_mode="Markdown"
        )
        set_single_bot_message(context, sent.message_id)
        return

    if is_expired_or_old_screenshot(update.message) or is_screenshot_already_used_today(photo_obj.file_unique_id):
        context.user_data.pop("qr_generated_for", None)
        await replace_bot_message(context, chat_id)
        sent = await update.message.reply_text(
            "❌ **Payment Rejected!**\n\nSirf fresh payment ka screenshot hi bhej sakte hain. Purana ya duplicate photo allowed nahi hai.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]),
            parse_mode="Markdown"
        )
        set_single_bot_message(context, sent.message_id)
        return

    context.user_data.pop("qr_generated_for", None)
    pkg = PACKAGES[qr_pkg_key]
    price_str = format_price(pkg)
    user = update.effective_user

    await replace_bot_message(context, chat_id)
    sent = await update.message.reply_text(
        f"⏳ **Screenshot Verification Pending!**\n\n📦 **Package:** {pkg['name']}\n💸 **Offer Price:** **{price_str}**\n✨ Approve hone ke baad link milega.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]]),
        parse_mode="Markdown"
    )
    set_single_bot_message(context, sent.message_id)

    try:
        admin_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{qr_pkg_key}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}_{qr_pkg_key}")
        ]])
        await context.bot.send_photo(
            chat_id=ADMIN_USER_ID,
            photo=photo_obj.file_id,
            caption=f"📥 **Payment Screenshot Verification**\n\n👤 **User:** {user.full_name} (`{user.id}`)\n📦 **Package:** {pkg['name']}\n💸 **Offer Price:** **{price_str}**",
            reply_markup=admin_kb,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Admin send error: {e}")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setphoto", process_photo_setting))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.VIDEO, handle_admin_video))
telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_media))

render_url = os.getenv("RENDER_EXTERNAL_URL")
if render_url:
    try:
        asyncio.run_coroutine_threadsafe(
            telegram_app.bot.set_webhook(url=f"{render_url.rstrip('/')}/{TELEGRAM_BOT_TOKEN}"), loop
        ).result(timeout=15)
    except Exception as e:
        print(f"Webhook setup error: {e}")


@app.route("/")
def home():
    return "Telegram Bot Webhook Server is Running!"


@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run_coroutine_threadsafe(telegram_app.process_update(update), loop).result(timeout=30)
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
