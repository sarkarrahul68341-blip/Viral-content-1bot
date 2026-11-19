import os
import asyncio
import threading
import urllib.parse
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9210267090:AAFGulP572uIzyKPEGVa01y7HuR9xt2adio")

UPI_ID = os.getenv("UPI_ID", "Puja6489@ptyes")
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "All Max Content Bot")

SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
ADMIN_USER_ID = 8776203848

# Permanent Channel Button Link & Name
PERMANENT_CHANNEL_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
PERMANENT_BUTTON_NAME = "Join Demo 2"

# Welcome (Main Menu) ki photo
DEFAULT_PHOTO = "AgACAgUAAxkBAAIKmWr-ocEknsMPFV0Ua2SDhjUpjx8SAAKzEmsbhy35V-O7-QS5ebgsAQADAgADeAADPQQ"

# Saare 8 packages par VIP New.jpg set rahegi
PACKAGE_PHOTO = "VIP New.jpg"

# ==================== PERMANENT STORAGE (Videos Set) ====================
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

DYNAMIC_STORAGE = {
    "welcome_photo": DEFAULT_PHOTO
}

# ==================== 8 FILES CONFIGURATION ====================
PACKAGES = {
    "file_1": {"name": "⭐ 01 All mix content VIP Access", "mrp": 499, "price": 249, "price_badge": "₹499 ➡️ 💎 ₹249", "btn_emoji": "👑", "link": "https://t.me/+s4Zzmwni59diNjU1", "photo": PACKAGE_PHOTO},
    "file_2": {"name": "🔑 02 Rap & Big File VD", "mrp": 199, "price": 89, "price_badge": "₹199 ➡️ ⚡ ₹89", "btn_emoji": "🎬", "link": "https://t.me/+_AILkUGhVnVkMzBl", "photo": PACKAGE_PHOTO},
    "file_3": {"name": "🔑 03 Mom and Son Real Sex", "mrp": 99, "price": 45, "price_badge": "₹99 ➡️ 🔥 ₹45", "btn_emoji": "💋", "link": "https://t.me/+qjTxEmHC-z4wMzE1", "photo": PACKAGE_PHOTO},
    "file_4": {"name": "🔞 04 Insta viral reels and sex", "mrp": 99, "price": 40, "price_badge": "₹99 ➡️ ✨ ₹40", "btn_emoji": "📱", "link": "https://t.me/+LmzeU14SK_I0MGY9", "photo": PACKAGE_PHOTO},
    "file_5": {"name": "🔥 05 Ganga bath group join", "mrp": 399, "price": 199, "price_badge": "₹399 ➡️ 👑 ₹199", "btn_emoji": "🌊", "link": "https://t.me/+jMs1EZ3RLSc1Yjhl", "photo": PACKAGE_PHOTO},
    "file_6": {"name": "🔥 06 Bath camera hidden", "mrp": 129, "price": 55, "price_badge": "₹129 ➡️ 💥 ₹55", "btn_emoji": "🎥", "link": "https://t.me/+G4yBWASYMzYzOTc9", "photo": PACKAGE_PHOTO},
    "file_7": {"name": "🔥 07 CP girl real fuke", "mrp": 149, "price": 65, "price_badge": "₹149 ➡️ 🌟 ₹65", "btn_emoji": "✨", "link": "https://t.me/+f9i3BlsoUeZiZmY1", "photo": PACKAGE_PHOTO},
    "file_8": {"name": "❤️ 08 Sister and brother sex", "mrp": 79, "price": 30, "price_badge": "₹79 ➡️ 💖 ₹30", "btn_emoji": "❤️", "link": "https://t.me/+BYOIdmg4w3c2MjQ1", "photo": PACKAGE_PHOTO},
}

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Dedicated background event loop thread
loop = asyncio.new_event_loop()


def _start_loop(target_loop):
    asyncio.set_event_loop(target_loop)
    target_loop.run_forever()


threading.Thread(target=_start_loop, args=(loop,), daemon=True).start()
asyncio.run_coroutine_threadsafe(telegram_app.initialize(), loop).result(timeout=30)


def format_price(pkg):
    return pkg.get("price_badge", f"💎 ₹{pkg['price']}")


def generate_upi_qr(amount, pkg_name, order_id):
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
    keyboard = []
    for key, pkg in PACKAGES.items():
        badge = format_price(pkg)
        btn_emoji = pkg.get("btn_emoji", "✨")
        keyboard.append([
            InlineKeyboardButton(f"{btn_emoji} {pkg['name']} • {badge} 👉", callback_data=key)
        ])

    keyboard.append([InlineKeyboardButton("🅵🆁🅴🅴   __   🅳🅴🅼🅾", callback_data="demo_1")])
    keyboard.append([InlineKeyboardButton("💬 Help & Support Desk", url=SUPPORT_LINK)])

    return InlineKeyboardMarkup(keyboard)


# ==================== HANDLERS ====================
async def start(update: Update, context):
    caption = (
        "❤️ **Welcome to All Max Content Bot!** ❤️\n\n"
        "🔥 **Special Discount Offer Chal Raha Hai!** Niche diye gaye packages mein se apna pasandida option select karein:\n"
    )
    current_photo = DYNAMIC_STORAGE.get("welcome_photo", DEFAULT_PHOTO)

    if update.callback_query:
        query = update.callback_query
        try:
            await query.message.delete()
        except Exception:
            pass
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=current_photo,
            caption=caption,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_photo(
            photo=current_photo,
            caption=caption,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )


async def process_photo_setting(update: Update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("⛔ Sirf admin hi photo update kar sakta hai.")
        return

    if not update.message.photo:
        await update.message.reply_text("⚠️ Kripya photo ke sath `/setphoto` likhein.")
        return

    photo_file = update.message.photo[-1].file_id
    DYNAMIC_STORAGE["welcome_photo"] = photo_file

    await update.message.reply_text(
        f"✅ **Welcome (Main Menu) ki photo update ho gayi hai!**\n\n"
        f"📋 **Is File ID ko copy karke code mein `DEFAULT_PHOTO` par daal sakte hain:**\n\n`{photo_file}`",
        parse_mode="Markdown"
    )


async def handle_admin_video(update: Update, context):
    if not update.message or not update.message.video:
        return

    if update.effective_user.id != ADMIN_USER_ID:
        return

    video_file_id = update.message.video.file_id
    PERMANENT_VIDEOS[10] = video_file_id

    await update.message.reply_text(
        "✅ **Demo 10 ki video update ho gayi hai!**\n\n"
        "📋 **Is File ID ko copy karke code mein `PERMANENT_VIDEOS[10]` par paste kar lein:**\n\n"
        f"`{video_file_id}`",
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "main_menu":
        await start(update, context)
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
            nav_buttons.append([
                InlineKeyboardButton("🔥👑 Get Full VIP Access • ₹499 ➡️ 💎 ₹249 🚀", callback_data="file_1")
            ])

        nav_buttons.append([InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")])
        nav_buttons.append([InlineKeyboardButton(PERMANENT_BUTTON_NAME, url=PERMANENT_CHANNEL_LINK)])

        keyboard = InlineKeyboardMarkup(nav_buttons)

        if index == 10:
            text = (
                f"🎬 **Demo Clip {index} / 10 (Last Demo)**\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                "✨ Saare demo clips khatam ho gaye! Full VIP collection ke liye niche button par click karein."
            )
        else:
            text = (
                f"🎬 **Demo Clip {index} / 10**\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                f"✨ Yeh hamari demo clip number {index} hai. Quality check karein!"
            )

        try:
            await query.message.delete()
        except Exception:
            pass

        video_file_id = PERMANENT_VIDEOS.get(index)
        current_photo = DYNAMIC_STORAGE.get("welcome_photo", DEFAULT_PHOTO)

        if video_file_id:
            try:
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=video_file_id,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            except Exception as e:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"❌ Error sending video: {str(e)}",
                    reply_markup=keyboard
                )
        else:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=current_photo,
                caption=text + "\n\n*(Yeh video abhi upload nahi ki gayi hai.)*",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        context.user_data["selected_pkg"] = data
        pkg_photo_path = pkg["photo"]
        price_str = format_price(pkg)

        text = (
            "🔥💎 **SELECTED VIP PACKAGE** 💎🔥\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"📦 **Package:** {pkg['name']}\n"
            f"💸 **Offer Price:** **{price_str}**\n\n"
            "✨ **Payment karne ke liye niche diye gaye button par click karein:** 👇"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💳 ⚡ Pay Now • {price_str} 🔥", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]
        ])

        try:
            await query.message.delete()
        except Exception:
            pass

        try:
            if pkg_photo_path and os.path.exists(pkg_photo_path):
                with open(pkg_photo_path, "rb") as photo_file:
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=photo_file,
                        caption=text,
                        reply_markup=keyboard,
                        parse_mode="Markdown"
                    )
            else:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=DEFAULT_PHOTO,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
        except Exception as e:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=text + f"\n\n*(Error: {str(e)})*",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        return

    elif data.startswith("pay_"):
        file_key = data.replace("pay_", "")
        pkg = PACKAGES.get(file_key)
        if not pkg:
            await query.message.reply_text("⚠️ Package nahi mila.")
            return

        context.user_data["selected_pkg"] = file_key
        context.user_data["qr_generated_for"] = file_key
        qr_file_path = None
        price_str = format_price(pkg)

        try:
            qr_file_path = generate_upi_qr(pkg["price"], pkg["name"], user_id)
            caption = (
                "🚨📱 **SCAN & PAY INSTRUCTIONS** 📱🚨\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                f"📦 **Package:** {pkg['name']}\n"
                f"💸 **Amount to Pay:** **{price_str}**\n\n"
                f"1️⃣ Is QR Code ko scan karke **₹{pkg['price']}** pay karein (`{UPI_ID}`).\n"
                f"2️⃣ Payment karne ke baad is chat mein **Payment ka Screenshot** bhejien taaki aapko turant link mil sake."
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]
            ])

            try:
                await query.message.delete()
            except Exception:
                pass

            with open(qr_file_path, "rb") as photo:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=photo,
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
        except Exception as e:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"❌ Error generating QR code: {str(e)}"
            )
        finally:
            if qr_file_path and os.path.exists(qr_file_path):
                try:
                    os.remove(qr_file_path)
                except Exception:
                    pass
        return


async def handle_media(update: Update, context):
    if not update.message.photo:
        return

    caption_text = (update.message.caption or "").lower()

    if "setphoto" in caption_text:
        await process_photo_setting(update, context)
        return

    qr_pkg_key = context.user_data.get("qr_generated_for")
    if not qr_pkg_key or qr_pkg_key not in PACKAGES:
        await update.message.reply_text(
            "⚠️ **Direct Photo Allowed Nahi Hai!**\n\n"
            "Kripya pehle Main Menu se package chunein aur **Pay Now** par click karke QR code generate karein, uske baad payment screenshot bhejein.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ]),
            parse_mode="Markdown"
        )
        return

    pkg = PACKAGES[qr_pkg_key]
    price_str = format_price(pkg)

    text = (
        "📸 **Screenshot Received Successfully!**\n\n"
        f"🎉 **Package:** {pkg['name']}\n"
        f"💸 **Offer Price:** **{price_str}**\n"
        "✨ Aapka payment screenshot mil gaya hai. Niche diye gaye button se apna VIP Access link kholen:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 🔓 Access VIP Content Link 🚀", url=pkg["link"])],
        [InlineKeyboardButton("🔙 🏠 Back to Main Menu", callback_data="main_menu")]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setphoto", process_photo_setting))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.VIDEO, handle_admin_video))
telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_media))


def setup_webhook():
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        clean_url = render_url.rstrip("/")
        webhook_url = f"{clean_url}/{TELEGRAM_BOT_TOKEN}"
        try:
            future = asyncio.run_coroutine_threadsafe(
                telegram_app.bot.set_webhook(url=webhook_url), loop
            )
            future.result(timeout=15)
        except Exception as e:
            print(f"Webhook setup error: {e}")


setup_webhook()


# ==================== FLASK ROUTES ====================
@app.route("/")
def home():
    return "Telegram Bot Webhook Server is Running!"


@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, telegram_app.bot)
    future = asyncio.run_coroutine_threadsafe(telegram_app.process_update(update), loop)
    future.result(timeout=30)
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
            
