import os
import asyncio
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
UPI_ID = "Puja6489@ptyes"
BUSINESS_NAME = "All Max Content Bot"

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

# ==================== 8 PACKAGES CONFIGURATION ====================
PACKAGES = {
    "pkg_1": {"name": "01 CP Video and File", "price": 249},
    "pkg_2": {"name": "02 Rap & CP & Big File VD", "price": 89},
    "pkg_3": {"name": "03 Mom and Son Real Sex", "price": 45},
    "pkg_4": {"name": "04 Insta viral reels and sex", "price": 30},
    "pkg_5": {"name": "05 Ganga bath group join", "price": 199},
    "pkg_6": {"name": "06 CP Bath camera hidden", "price": 55},
    "pkg_7": {"name": "07 Pakistani girl real fuke", "price": 49},
    "pkg_8": {"name": "08 Sister and brother sex", "price": 30},
}

# ==================== KEYBOARD FUNCTION ====================
def get_main_menu_keyboard():
    keyboard = []
    for key, pkg in PACKAGES.items():
        keyboard.append([InlineKeyboardButton(f"🔑 {pkg['name']} --------- Rs.{pkg['price']}", callback_data=key)])
    return InlineKeyboardMarkup(keyboard)

# ==================== QR CODE GENERATOR ====================
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
    text = "✨ **All Max Content Bot**\n\nSelect a package below to purchase:"
    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await start(update, context)
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        user_id = query.from_user.id
        
        qr_file_path = generate_upi_qr(pkg["price"], pkg["name"], user_id)
        
        caption = (
            f"📦 **{pkg['name']}**\n"
            f"💰 Price: **Rs.{pkg['price']}**\n\n"
            f"📱 **Payment Instructions:**\n"
            f"1. Is QR Code ko scan karke **Rs.{pkg['price']}** pay karein.\n"
            f"2. Payment ke baad screenshot yahan bhejein."
        )
        
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]])
        
        with open(qr_file_path, 'rb') as photo:
            await query.message.reply_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown")
            
        if os.path.exists(qr_file_path):
            os.remove(qr_file_path)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

# Global initialization flag
app_initialized = False

async def initialize_bot():
    global app_initialized
    if not app_initialized:
        await telegram_app.initialize()
        await telegram_app.start()
        app_initialized = True

# ==================== FLASK ROUTES ====================
@app.route('/')
def home():
    return "Telegram Bot Webhook Server is Running!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, telegram_app.bot)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def process():
        await initialize_bot()
        await telegram_app.process_update(update)
        
    loop.run_until_complete(process())
    loop.close()
    
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
        
