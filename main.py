import os
import time
import asyncio
import threading
import urllib.parse
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN missing hai! Render Environment mein token set karein.")

UPI_ID = os.getenv("UPI_ID", "Puja6489@ptyes")
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "All Max Content Bot")
SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "8776203848"))
PERMANENT_CHANNEL_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
PERMANENT_BUTTON_NAME = "Join Demo 2"
DEFAULT_PHOTO = os.getenv("DEFAULT_PHOTO", "").strip()
PACKAGE_PHOTO = "VIP New.jpg"
BANNER_PHOTO = os.getenv("BANNER_PHOTO", PACKAGE_PHOTO).strip()
SCREENSHOT_VALIDITY_SECONDS = 24 * 60 * 60
USED_SCREENSHOTS = {}

PERMANENT_VIDEOS = {
    1: "", 2: "", 3: "", 4: "", 5: "",
    6: "", 7: "", 8: "", 9: "", 10: "",
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


async def _init_bot():
    await telegram_app.initialize()
    await telegram_app.start()


asyncio.run_coroutine_threadsafe(_init_bot(), loop).result(timeout=30)


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
        await clear_previous_view(context, chat_id, update.callback_query.message)
    else:
        await clear_previous_view(context, chat_id)
    sent = await send_main_menu(context, chat_id)
    remember_bot_message(context, sent.message_id)


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


async def handle_video_id(update: Update, context):
    if not update.message or not update.message.video:
        return
    vid_id = update.message.video.file_id
    if update.effective_user.id == ADMIN_USER_ID:
        PERMANENT_VIDEOS[10] = vid_id
        await update.message.reply_text(f"✅ **Demo 10 video update ho gayi!**\n\n`{vid_id}`", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"🎬 **Video File ID:**\n\n`{vid_id}`", parse_mode="Markdown")


async def callback_handler(update: Update, context):
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
                        [InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")],
                    ]),
                    parse_mode="Markdown",
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
                    parse_mode="Markdown",
                )
                try:
                    await query.edit_message_caption(caption=(query.message.caption or "") + "\n\n❌ **REJECTED**", parse_mode="Markdown")
                except Exception:
                    pass
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

        video_file_id = PERMANENT_VIDEOS.get(index, "").strip()
        if video_file_id:
            try:
                sent = await context.bot.send_video(
                    chat_id=chat_id, video=video_file_id, caption=text, reply_markup=keyboard, parse_mode="Markdown"
                )
                remember_bot_message(context, sent.message_id)
                return
            except BadRequest:
                pass

        fallback_photo = DYNAMIC_STORAGE.get("welcome_photo") or (PACKAGE_PHOTO if os.path.exists(PACKAGE_PHOTO) else "")
        sent = await send_photo_safe(context, chat_id, fallback_photo, text, keyboard)
        remember_bot_message(context, sent.message_id)
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
        await clear_previous_view(context, chat_id, query.message)
        sent = await send_photo_safe(context, chat_id, banner, text, keyboard)
        remember_bot_message(context, sent.message_id)
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
            caption = (
                f"🚨📱 **SCAN & PAY INSTRUCTIONS** 📱🚨\n"
                f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                f"📦 **Package:** {pkg['name']}\n"
                f"💸 **Amount to Pay:** **{price_str}**\n\n"
                f"1️⃣ Is QR Code ko scan karke **₹{pkg['price']}** pay karein (`{UPI_ID}`).\n"
                f"2️⃣ Payment karne ke baad is chat mein **Payment ka Screenshot** bhejien. Approve hone ke baad link milega."
            )
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]])
            await clear_previous_view(context, chat_id, query.message)
            with open(qr_file_path, "rb") as photo:
                sent = await context.bot.send_photo(
                    chat_id=chat_id, photo=photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown"
                )
            remember_bot_message(context, sent.message_id)
        finally:
            if qr_file_path and os.path.exists(qr_file_path):
                try:
                    os.remove(qr_file_path)
                except Exception:
                    pass


async def handle_media(update: Update, context):
    if not update.message or not update.message.photo:
        return
    caption_text = (update.message.caption or "").strip().lower()
    if "/setbanner" in caption_text or "setbanner" in caption_text:
        await set_banner_photo(update, context)
        return

    chat_id = update.effective_chat.id
    qr_pkg_key = context.user_data.get("qr_generated_for")
    if not qr_pkg_key or qr_pkg_key not in PACKAGES:
        await delete_tracked_bot_messages(context, chat_id)
        sent = await update.message.reply_text(
            "❌ Sorry ji, abhi tak aapki payment receive nahi hui hai. Kripya pehle package select karke Pay Now se payment karein, uske baad screenshot bhejein.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]),
        )
        remember_bot_message(context, sent.message_id)
        return

    photo_obj = update.message.photo[-1]
    if is_expired_or_old_screenshot(update.message) or is_screenshot_already_used_today(photo_obj.file_unique_id):
        await delete_tracked_bot_messages(context, chat_id)
        sent = await update.message.reply_text(
            "❌ Sorry ji, abhi tak aapki payment receive nahi hui hai. Kripya pehle package select karke Pay Now se payment karein, uske baad screenshot bhejein.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]),
        )
        remember_bot_message(context, sent.message_id)
        return

    context.user_data.pop("qr_generated_for", None)
    pkg = PACKAGES[qr_pkg_key]
    price_str = format_price(pkg)
    user = update.effective_user

    await delete_tracked_bot_messages(context, chat_id)
    sent = await update.message.reply_text(
        f"⏳ **Screenshot Verification Pending!**\n\n📦 **Package:** {pkg['name']}\n💸 **Offer Price:** **{price_str}**\n✨ Approve hone ke baad link milega.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]]),
        parse_mode="Markdown",
    )
    remember_bot_message(context, sent.message_id)

    try:
        admin_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{qr_pkg_key}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}_{qr_pkg_key}"),
        ]])
        await context.bot.send_photo(
            chat_id=ADMIN_USER_ID,
            photo=photo_obj.file_id,
            caption=f"📥 **Payment Screenshot Verification**\n\n👤 **User:** {user.full_name} (`{user.id}`)\n📦 **Package:** {pkg['name']}\n💸 **Offer Price:** **{price_str}**",
            reply_markup=admin_kb,
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Admin send error: {e}")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setbanner", set_banner_photo))
telegram_app.add_handler(CallbackQueryHandler(callback_handler))
telegram_app.add_handler(MessageHandler(filters.VIDEO, handle_video_id))
telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_media))


def _register_webhook_async():
    render_url = os.getenv("RENDER_EXTERNAL_URL") or "https://viral-content-1bot-1.onrender.com"
    webhook_url = f"{render_url.rstrip('/')}/{TELEGRAM_BOT_TOKEN}"
    try:
        fut = asyncio.run_coroutine_threadsafe(telegram_app.bot.set_webhook(url=webhook_url), loop)
        fut.result(timeout=20)
        print(f"Webhook set: {webhook_url}")
    except Exception as e:
        print(f"Webhook setup error: {e}")


threading.Thread(target=_register_webhook_async, daemon=True).start()


@app.route("/")
def home():
    return "Bot Webhook Server is Running!"


@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        payload = request.get_json(force=True, silent=True) or {}
        if not payload:
            return "OK", 200
        update = Update.de_json(payload, te
