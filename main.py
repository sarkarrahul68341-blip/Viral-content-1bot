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

# Permanent Channel Button Link & Name (Single Emoji)
PERMANENT_CHANNEL_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
PERMANENT_BUTTON_NAME = "📢 Join VIP Channel"

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

# ==================== 8 FILES CONFIGURATION (SINGLE OFFER, SINGLE EMOJI & SIZE) ====================
PACKAGES = {
    "file_1": {"name": "01 All mix content VIP Access", "size": "4.5 GB", "mrp": 499, "price": 249, "emoji": "💎", "link": "https://t.me/+s4Zzmwni59diNjU1", "photo": PACKAGE_PHOTO},
    "file_2": {"name": "02 Rap & Big File VD", "size": "2.2 GB", "mrp": 199, "price": 89, "emoji": "⚡", "link": "https://t.me/+_AILkUGhVnVkMzBl", "photo": PACKAGE_PHOTO},
    "file_3": {"name": "03 Mom and Son Real Sex", "size": "950 MB", "mrp": 99, "price": 45, "emoji": "🔥", "link": "https://t.me/+qjTxEmHC-z4wMzE1", "photo": PACKAGE_PHOTO},
    "file_4": {"name": "04 Insta viral reels and sex", "size": "800 MB", "mrp": 99, "price": 40, "emoji": "✨", "link": "https://t.me/+LmzeU14SK_I0MGY9", "photo": PACKAGE_PHOTO},
    "file_5": {"name": "05 Ganga bath group join", "size": "3.8 GB", "mrp": 399, "price": 199, "emoji": "🌊", "link": "https://t.me/+jMs1EZ3RLSc1Yjhl", "photo": PACKAGE_PHOTO},
    "file_6": {"name": "06 Bath camera hidden", "size": "1.4 GB", "mrp": 129, "price": 55, "emoji": "🎥", "link": "https://t.me/+G4yBWASYMzYzOTc9", "photo": PACKAGE_PHOTO},
    "file_7": {"name": "07 CP girl real fuke", "size": "1.6 GB", "mrp": 149, "price": 65, "emoji": "🌟", "link": "https://t.me/+f9i3BlsoUeZiZmY1", "photo": PACKAGE_PHOTO},
    "file_8": {"name": "08 Sister and brother sex", "size": "650 MB", "mrp": 79, "price": 30, "emoji": "❤️", "link": "https://t.me/+BYOIdmg4w3c2MjQ1", "photo": PACKAGE_PHOTO},
}

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Dedicated background event loop thread
loop = asyncio.new_event_loop()
_initialized = False
_init_lock = threading.Lock()


def _start_loop(target_loop):
    asyncio.set_event_loop(target_loop)
    target_loop.run_forever()


threading.Thread(target=_start_loop, args=(loop,), daemon=True).start()


def ensure_bot_ready():
    global _initialized
    if _initialized:
        return
    with _init_lock:
        if _initialized:
            return
        try:
            future = asyncio.run_coroutine_threadsafe(telegram_app.initialize(), loop)
            future.result(timeout=30)
            _initialized = True
            setup_webhook()
        except Exception as e:
            print(f"Bot initialization error: {e}")


def format_price_text(pkg):
    return f"₹{pkg['mrp']} ➡️ **₹{pkg['price']}**"


def format_price_button(pkg):
    return f"₹{pkg['mrp']} ➡️ ₹{pkg['price']}"


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
        emoji = pkg.get("emoji", "💎")
        size_str = pkg.get("size", "")
        price_badge = format_price_button(pkg)
        size_part = f" [{size_str}]" if size_str else ""
        keyboard.append([
            InlineKeyboardButton(f"{emoji} {pkg['name']}{size_part} • {price_badge}", callback_data=key)
        ])

    keyboard.append([InlineKeyboardButton("🎬 Watch Demo Videos", callback_data="demo_1")])
    keyboard.append([InlineKeyboardButton("💬 Help & Support", url=SUPPORT_LINK)])

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

    if data.startswith("approve_") or data.startswith("reject_"):
        if user_id != ADMIN_USER_ID:
            await query.answer("⛔ Sirf admin hi approve ya reject kar sakta hai.", show_alert=True)
            return

        action, target_user_str, file_key = data.split("_", 2)
        target_user_id = int(target_user_str)
        pkg = PACKAGES.get(file_key, PACKAGES["file_1"])
        emoji = pkg.get("emoji", "💎")
        price_str = format_price_text(pkg)

        if action == "approve":
            user_msg = (
                "✅ **Payment Approved!**\n\n"
                f"{emoji} **Package:** {pkg['name']}\n"
                f"💸 **Price:** {price_str}\n"
                "🎉 Aapka payment verify ho gaya hai. Niche diye gaye button se apna VIP Access link kholen:"
            )
            user_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Access VIP Content Link", url=pkg["link"])],
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ])
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=user_msg,
                    reply_markup=user_keyboard,
                    parse_mode="Markdown"
                )
            except Exception as e:
                await context.bot.send_message(
                    chat_id=ADMIN_USER_ID,
                    text=f"⚠️ User ko message bhejne mein error aaya: {str(e)}"
                )

            try:
                await query.edit_message_caption(
                    caption=(query.message.caption or "") + "\n\n✅ **APPROVED & LINK SENT**",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
        else:
            reject_msg = (
                "❌ **Payment Screenshot Rejected!**\n\n"
                f"{emoji} **Package:** {pkg['name']}\n"
                f"💸 **Required Amount:** {price_str}\n"
                "⚠️ Kripya sahi payment ka clear screenshot bhejein ya help ke liye Support se sampark karein."
            )
            reject_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Help & Support", url=SUPPORT_LINK)],
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ])
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=reject_msg,
                    reply_markup=reject_keyboard,
                    parse_mode="Markdown"
                )
            except Exception:
                pass

            try:
                await query.edit_message_caption(
                    caption=(query.message.caption or "") + "\n\n❌ **REJECTED**",
                    parse_mode="Markdown"
                )
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
            row.append(InlineKeyboardButton("⬅️ Prev Clip", callback_data=f"demo_{index - 1}"))
        if index < 10:
            row.append(InlineKeyboardButton("Next Clip ➡️", callback_data=f"demo_{index + 1}"))

        if row:
            nav_buttons.append(row)

        if index == 10:
            vip_pkg = PACKAGES["file_1"]
            nav_buttons.append([
                InlineKeyboardButton(
                    f"🔥 Get Full VIP Access • {format_price_button(vip_pkg)}",
                    callback_data="file_1"
                )
            ])

        nav_buttons.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
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
        context.user_data["last_pkg"] = data
        pkg_photo_path = pkg["photo"]
        emoji = pkg.get("emoji", "💎")
        size_str = pkg.get("size", "")
        price_str = format_price_text(pkg)
        price_btn = format_price_button(pkg)

        size_line = f"📦 **Size:** {size_str}\n" if size_str else ""

        text = (
            "🔥 **SELECTED VIP PACKAGE** 🔥\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"{emoji} **Package:** {pkg['name']}\n"
            f"{size_line}"
            f"💸 **Offer Price:** {price_str}\n\n"
            "✨ **Payment karne ke liye niche diye gaye button par click karein:**"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💳 Pay Now • {price_btn}", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
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

        context.user_data["last_pkg"] = file_key
        qr_file_path = None
        emoji = pkg.get("emoji", "💎")
        size_str = pkg.get("size", "")
        price_str = format_price_text(pkg)
        size_line = f"📦 **Size:** {size_str}\n" if size_str else ""

        try:
            qr_file_path = generate_upi_qr(pkg["price"], pkg["name"], user_id)
            caption = (
                "📱 **SCAN & PAY INSTRUCTIONS** 📱\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                f"{emoji} **Package:** {pkg['name']}\n"
                f"{size_line}"
                f"💸 **Amount to Pay:** {price_str}\n\n"
                f"1️⃣ Is QR Code ko scan karke **₹{pkg['price']}** pay karein (`{UPI_ID}`).\n"
                f"2️⃣ Payment karne ke baad is chat mein **Payment ka Screenshot** bhejien taaki verification ke baad aapko link mil sake."
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
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

    user = update.effective_user
    last_file_key = context.user_data.get("last_pkg", "file_1")
    pkg = PACKAGES.get(last_file_key, PACKAGES["file_1"])
    emoji = pkg.get("emoji", "💎")
    price_str = format_price_text(pkg)
    photo_id = update.message.photo[-1].file_id

    await update.message.reply_text(
        "⏳ **Screenshot Verification Pending!**\n\n"
        f"{emoji} **Package:** {pkg['name']}\n"
        f"💸 **Price:** {price_str}\n"
        "✨ Aapka payment screenshot admin ke paas check hone ke liye bhej diya gaya hai. Approve hote hi aapko VIP link mil jayega.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ]),
        parse_mode="Markdown"
    )

    admin_caption = (
        "📥 **New Payment Screenshot For Review**\n\n"
        f"👤 **User:** {user.full_name} (`{user.id}`)\n"
        f"{emoji} **Package:** {pkg['name']}\n"
        f"💸 **Price:** {price_str}"
    )
    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve & Send Link", callback_data=f"approve_{user.id}_{last_file_key}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}_{last_file_key}")
        ]
    ])
    try:
        await context.bot.send_photo(
            chat_id=ADMIN_USER_ID,
            photo=photo_id,
            caption=admin_caption,
            reply_markup=admin_keyboard,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Admin notification error: {e}")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setphoto", process_photo_setting))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.VIDEO, handle_admin_video))
telegram_app.add_han
