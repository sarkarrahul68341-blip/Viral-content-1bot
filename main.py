import os
import asyncio
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = "9210267090:AAFGulP572uIzyKPEGVa01y7HuR9xt2adio"

UPI_ID = "Puja6489@ptyes"
BUSINESS_NAME = "All Max Content Bot"

DEMO_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"

# Default welcome photo agar user set na kare
WELCOME_PHOTO_FILE_ID = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# ==================== 8 PACKAGES CONFIGURATION ====================
PACKAGES = {
    "pkg_1": {"name": "⭐ 01 All mix content VIP Access", "price": 249, "link": "https://t.me/+s4Zzmwni59diNjU1"},
    "pkg_2": {"name": "🔑 02 Rap & Big File VD", "price": 1, "link": "https://t.me/+f9i3BlsoUeZiZmY1"},
    "pkg_3": {"name": "🔑 03 Mom and Son Real Sex", "price": 45, "link": "https://t.me/+cKmPMnPz-UI4Y2NI"},
    "pkg_4": {"name": "🔞 04 Insta viral reels and sex", "price": 30, "link": "https://t.me/+LmzeU14SK_I0MGY9"},
    "pkg_5": {"name": "🔥 05 Ganga bath group join", "price": 199, "link": "https://t.me/+jMs1EZ3RLSc1Yjhl"},
    "pkg_6": {"name": "🔥 06 Bath camera hidden", "price": 55, "link": "https://t.me/+G4yBWASYMzYzOTc9"},
    "pkg_7": {"name": "🔥 07 Pakistani girl real fuke", "price": 49, "link": "https://t.me/+BYOldmg4w3c2MjQ1"},
    "pkg_8": {"name": "❤️ 08 Sister and brother sex", "price": 30, "link": "https://t.me/+BYOldmg4w3c2MjQ1"},
}

def get_main_menu_keyboard():
    keyboard = []
    for key, pkg in PACKAGES.items():
        keyboard.append([InlineKeyboardButton(f"{pkg['name']} 🌟 ─── Rs.{pkg['price']}", callback_data=key)])
    
    keyboard.append([InlineKeyboardButton("🚀 Free Demo & Trial", url=DEMO_LINK)])
    keyboard.append([InlineKeyboardButton("💬 Help & Support Chat", url=SUPPORT_LINK)])
    
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
    global WELCOME_PHOTO_FILE_ID
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
            photo=WELCOME_PHOTO_FILE_ID,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_photo(
            photo=WELCOME_PHOTO_FILE_ID,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def set_photo(update: Update, context):
    global WELCOME_PHOTO_FILE_ID
    if update.message.photo:
        photo_file = update.message.photo[-1].file_id
        WELCOME_PHOTO_FILE_ID = photo_file
        await update.message.reply_text("✅ **Welcome Photo successfully update ho gayi hai!** Ab /start dabakar check karein.")
    else:
        await update.message.reply_text("⚠️ Kripya photo ke sath caption mein `/setphoto` likhkar bhejein.")

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await start(update, context)
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        context.user_data['last_pkg'] = data
        
        text = (
            f"📦 **{pkg['name']}**\n"
            f"💰 Price: **Rs.{pkg['price']}**\n\n"
            f"✨ Payment karne ke liye niche diye gaye button par click karein:"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Pay Now (UPI QR)", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ])
        
        try:
            await query.message.delete()
        except Exception:
            pass
            
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    elif data.startswith("pay_"):
        pkg_key = data.replace("pay_", "")
        pkg = PACKAGES[pkg_key]
        context.user_data['last_pkg'] = pkg_key
        user_id = query.from_user.id
        
        try:
            qr_file_path = generate_upi_qr(pkg["price"], pkg["name"], user_id)
            caption = (
                f"📦 **{pkg['name']}**\n"
                f"💰 Price: **Rs.{pkg['price']}**\n\n"
                f"📱 **Payment Instructions:**\n"
                f"1️⃣ Is QR Code ko scan karke **Rs.{pkg['price']}** pay karein (`{UPI_ID}`).\n"
                f"2️⃣ Payment karne ke baad is chat mein **Payment ka Screenshot (Photo)** bhejien taaki aapko turant link mil sake."
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
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
                text=f"❌ Error generating QR code: {str(e)}"
            )

async def handle_photo(update: Update, context):
    if update.message.caption and "/setphoto" in update.message.caption:
        await set_photo(update, context)
        return

    last_pkg_key = context.user_data.get('last_pkg', 'pkg_1')
    pkg = PACKAGES.get(last_pkg_key, PACKAGES['pkg_1'])

    text = (
        "📸 **Screenshot Received Successfully!**\n\n"
        f"🎉 Package: **{pkg['name']}**\n"
        "✨ Aapka payment screenshot mil gaya hai. Niche diye gaye button se apna VIP Access link kholen:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Access VIP Content Link", url=pkg["link"])],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setphoto", set_photo))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# ==================== FLASK ROUTES ====================
@app.route('/')
def home():
    return "Telegram Bot Webhook Server is Running!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, telegram_app.bot)
    
    async def run_update():
        async with telegram_app:
            await telegram_app.process_update(update)

    asyncio.run(run_update())
    return "OK", 200

# ==================== MAIN RUNNER ====================
if __name__ == '__main__':
    RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_EXTERNAL_URL:
        import urllib.request
        webhook_url = f"{RENDER_EXTERNAL_URL}/{TELEGRAM_BOT_TOKEN}"
        urllib.request.urlopen(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
                
