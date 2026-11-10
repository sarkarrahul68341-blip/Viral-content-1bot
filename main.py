import os
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
UPI_ID = "Puja6489@ptyes"
BUSINESS_NAME = "All Max Content Bot"

DEMO_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
WELCOME_PHOTO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# ==================== 8 PACKAGES CONFIGURATION (WITH CUSTOM DESCRIPTIONS) ====================
PACKAGES = {
    "pkg_1": {
        "name": "🔑 01 Video and File", 
        "price": 249, 
        "desc": "Yahan aapko sabse best high quality video files aur premium content milega! Niche 'Pay Now' par click karke payment karein.",
        "link": "https://t.me/+iLoNw5R4Qwk5MGI1"
    },
    "pkg_2": {
        "name": "🔑 02 Rap & Big File VD", 
        "price": 89, 
        "desc": "Yahan aapko heavy rap videos aur badi files ka direct access milega! Niche 'Pay Now' par click karein.",
        "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"
    },
    "pkg_3": {
        "name": "🔑 03 Mom and Son Real Sex", 
        "price": 45, 
        "desc": "Yahan aapko exclusive real content milne wala hai. Niche 'Pay Now' par click karke aage badhein!",
        "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"
    },
    "pkg_4": {
        "name": "🔞 04 Insta viral reels and sex", 
        "price": 30, 
        "desc": "Yahan saari Insta viral reels aur hot clips milengi. Niche 'Pay Now' button par click karein!",
        "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"
    },
    "pkg_5": {
        "name": "🔥 05 Ganga bath group join", 
        "price": 199, 
        "desc": "Yahan aapko special Ganga bath group ka link aur exclusive content milega. Niche click karein!",
        "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"
    },
    "pkg_6": {
        "name": "🔥 06 Bath camera hidden", 
        "price": 55, 
        "desc": "Yahan hidden camera bath ki secret videos milengi. Niche 'Pay Now' par click karke payment karein.",
        "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"
    },
    "pkg_7": {
        "name": "🔥 07 Pakistani girl real fuke", 
        "price": 49, 
        "desc": "Yahan Pakistani viral aur real hot videos ka collection milega. Niche click karke aage badhein!",
        "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"
    },
    "pkg_8": {
        "name": "❤️ 08 Sister and brother sex", 
        "price": 30, 
        "desc": "Yahan aapko yeh special collection dekhne ko milega. Niche 'Pay Now' par click karke turant join karein!",
        "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"
    },
}

def get_main_menu_keyboard():
    keyboard = []
    for key, pkg in PACKAGES.items():
        keyboard.append([InlineKeyboardButton(f"{pkg['name']} --------- Rs.{pkg['price']}", callback_data=key)])
    
    keyboard.append([
        InlineKeyboardButton("🚀 Free Demo", url=DEMO_LINK),
        InlineKeyboardButton("💬 Help / Support", url=SUPPORT_LINK)
    ])
    return InlineKeyboardMarkup(keyboard)

def generate_upi_qr(amount, pkg_name, order_id):
    upi_uri = f"upi://pay?pa={UPI_ID}&pn={BUSINESS_NAME}&am={amount}&cu=INR&tn=Order_{order_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"qr_{order_id}.png"
    img.save(filename)
    return filename

# ==================== HANDLERS ====================
async def start(update: Update, context):
    reply_markup = get_main_menu_keyboard()
    caption = (
        "❤️ **Welcome to All Max Content Bot!** ❤️\n\n"
        "✨ Aapka yahan swagat hai! Niche diye gaye packages mein se apna pasandida option select karein:\n"
    )
    
    if update.callback_query:
        query = update.callback_query
        try:
            await query.message.delete()
        except Exception:
            pass
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=WELCOME_PHOTO_URL,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_photo(
            photo=WELCOME_PHOTO_URL,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await start(update, context)
        return

    # Har package ke click par uska special description aur 'Pay Now' option
    if data in PACKAGES:
        pkg = PACKAGES[data]
        text = (
            f"📦 **{pkg['name']}**\n"
            f"💰 Price: **Rs.{pkg['price']}**\n\n"
            f"📝 {pkg['desc']}\n\n"
            f"👉 Niche **Pay Now** par click karke payment karein:"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Pay Now", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ])
        
        try:
            if query.message.photo:
                await query.message.delete()
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            else:
                await query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        except Exception:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )

    elif data.startswith("pay_"):
        pkg_key = data.replace("pay_", "")
        pkg = PACKAGES[pkg_key]
        user_id = query.from_user.id
        
        try:
            qr_file_path = generate_upi_qr(pkg["price"], pkg["name"], user_id)
            caption = (
                f"📦 **{pkg['name']}**\n"
                f"💰 Price: **Rs.{pkg['price']}**\n\n"
                f"📱 **Payment Instructions:**\n"
                f"1. Is QR Code ko scan karke **Rs.{pkg['price']}** pay karein (`{UPI_ID}`).\n"
                f"2. Payment ke baad niche **Verify Payment** par click karein."
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Verify Payment", callback_data=f"verify_{pkg_key}")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
            ])
            
            try:
                await query.message.delete()
            except Exception:
                pass
                
            with open(qr_file_path, 'rb') as photo:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=photo,
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            if os.path.exists(qr_file_path):
                os.remove(qr_file_path)
        except Exception as e:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
    
