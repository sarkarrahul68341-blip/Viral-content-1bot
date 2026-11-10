import os
import asyncio
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
UPI_ID = "Puja6489@ptyes"
BUSINESS_NAME = "All Max Content Bot"

DEMO_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
WELCOME_PHOTO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# ==================== 8 PACKAGES WITH EMOJIS & LINKS ====================
PACKAGES = {
    "pkg_1": {"name": "⭐ 01 All mix content VIP Access", "price": 249, "link": "YAHAN_APNA_LINK_1_DALO"},
    "pkg_2": {"name": "🔑 02 Rap & Big File VD", "price": 89, "link": "YAHAN_APNA_LINK_2_DALO"},
    "pkg_3": {"name": "🔑 03 Mom and Son Real Sex", "price": 45, "link": "YAHAN_APNA_LINK_3_DALO"},
    "pkg_4": {"name": "🔞 04 Insta viral reels and sex", "price": 30, "link": "YAHAN_APNA_LINK_4_DALO"},
    "pkg_5": {"name": "🔥 05 Ganga bath group join", "price": 199, "link": "YAHAN_APNA_LINK_5_DALO"},
    "pkg_6": {"name": "🔥 06 Bath camera hidden", "price": 55, "link": "YAHAN_APNA_LINK_6_DALO"},
    "pkg_7": {"name": "🔥 07 Pakistani girl real fuke", "price": 49, "link": "YAHAN_APNA_LINK_7_DALO"},
    "pkg_8": {"name": "❤️ 08 Sister and brother sex", "price": 30, "link": "YAHAN_APNA_LINK_8_DALO"},
}

def get_main_menu_keyboard():
    keyboard = []
    for key, pkg in PACKAGES.items():
        keyboard.append([InlineKeyboardButton(f"{pkg['name']} 🌟 ─── Rs.{pkg['price']}", callback_data=key)])
    
    # Bade size (full-width) wale Demo aur Support buttons emojis ke sath
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

    if data in PACKAGES:
        pkg = PACKAGES[data]
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
        user_id = query.from_user.id
        
        try:
            qr_file_path = generate_upi_qr(pkg["price"], pkg["name"], user_id)
            caption = (
                f"📦 **{pkg['name']}**\n"
                f"💰 Price: **Rs.{pkg['price']}**\n\n"
                f"📱 **Payment Instructions:**\n"
                f"1️⃣ Is QR Code ko scan karke **Rs.{pkg['price']}** pay karein (`{UPI_ID}`).\n"
                f"2️⃣ Payment ke baad niche **Verify Payment** par click karein."
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Verify Payment", callback_data=f"verify_{pkg_key}")],
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

    elif data.startswith("verify_"):
        pkg_key = data.replace("verify_", "")
        pkg = PACKAGES[pkg_key]
        text = (
            f"🎉 **Payment Verified Successfully!** 🎉\n"
            f"📦 Package: **{pkg['name']}** (Rs.{pkg['price']})\n\n"
            f"✨ Aapka content link niche diya gaya hai. Button par click karke turant join karein:"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Access Content Link", url=pkg["link"])],
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

# Agar user screenshot (photo) bhejta hai, toh bot automatically emojis ke sath link aur Menu button de dega
async def handle_photo(update: Update, context):
    text = (
        "📸 **Screenshot Received Successfully!**\n\n"
        "✨ Aapka payment check ho gaya hai. Niche diye gaye button se content access karein ya menu par wapas jayen:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Access Content Link", url=PACKAGES["pkg_1"]["link"])],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

telegram_app.add_handler(CommandHandler("start", start))
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
    
