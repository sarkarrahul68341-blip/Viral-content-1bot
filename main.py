import os
import asyncio
import sqlite3
import re
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = "9210267090:AAFGulP572uIzyKPEGVa01y7HuR9xt2adio"

UPI_ID = "Puja6489@ptyes"
BUSINESS_NAME = "All Max Content Bot"

SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
ADMIN_USER_ID = 8776203848  # Aapki Admin ID

# Permanent Channel Button Link & Name
PERMANENT_CHANNEL_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
PERMANENT_BUTTON_NAME = "Join Channel"

# Welcome (Main Menu) ki default photo
DEFAULT_PHOTO = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

# Sabhi 8 packages par Vip1.jpg set kar diya hai
PACKAGE_PHOTO = "Vip1.jpg"

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
    10: "BAACAgUAAxkBAAIGPWr9SvKxI0Mk2KlITw5rCPYgc1HdAAL6IQAC08jpV0bXxX-172rIPQQ",
}

# Dynamic storage for Welcome Photo
DYNAMIC_STORAGE = {
    "welcome_photo": DEFAULT_PHOTO
}

# ==================== 8 FILES CONFIGURATION ====================
PACKAGES = {
    "file_1": {"name": "⭐ 01 All mix content VIP Access", "price": 249, "link": "https://t.me/+s4Zzmwni59diNjU1", "photo": PACKAGE_PHOTO},
    "file_2": {"name": "🔑 02 Rap & Big File VD", "price": 89, "link": "https://t.me/+_AILkUGhVnVkMzBl", "photo": PACKAGE_PHOTO},
    "file_3": {"name": "🔑 03 Mom and Son Real Sex", "price": 45, "link": "https://t.me/+qjTxEmHC-z4wMzE1", "photo": PACKAGE_PHOTO},
    "file_4": {"name": "🔞 04 Insta viral reels and sex", "price": 40, "link": "https://t.me/+LmzeU14SK_I0MGY9", "photo": PACKAGE_PHOTO},
    "file_5": {"name": "🔥 05 Ganga bath group join", "price": 199, "link": "https://t.me/+jMs1EZ3RLSc1Yjhl", "photo": PACKAGE_PHOTO},
    "file_6": {"name": "🔥 06 Bath camera hidden", "price": 55, "link": "https://t.me/+G4yBWASYMzYzOTc9", "photo": PACKAGE_PHOTO},
    "file_7": {"name": "🔥 07 CP girl real fuke", "price": 65, "link": "https://t.me/+f9i3BlsoUeZiZmY1", "photo": PACKAGE_PHOTO},
    "file_8": {"name": "❤️ 08 Sister and brother sex", "price": 30, "link": "https://t.me/+BYOIdmg4w3c2MjQ1", "photo": PACKAGE_PHOTO},
}

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# ==================== DATABASE FOR VIEWS ONLY ====================
def init_db():
    conn = sqlite3.connect('bot_views.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demo_stats (
            clip_id INTEGER PRIMARY KEY,
            views INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_views (
            user_id INTEGER,
            clip_id INTEGER,
            PRIMARY KEY (user_id, clip_id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def check_and_increment_view(user_id, clip_id):
    conn = sqlite3.connect('bot_views.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT views FROM demo_stats WHERE clip_id = ?', (clip_id,))
    row = cursor.fetchone()
    
    if not row:
        cursor.execute('INSERT INTO demo_stats (clip_id, views) VALUES (?, 0)', (clip_id,))
        conn.commit()
        current_views = 0
    else:
        current_views = row[0]

    if user_id != ADMIN_USER_ID:
        cursor.execute('SELECT * FROM user_views WHERE user_id = ? AND clip_id = ?', (user_id, clip_id))
        already_viewed = cursor.fetchone()
        
        if not already_viewed:
            current_views += 1
            cursor.execute('UPDATE demo_stats SET views = ? WHERE clip_id = ?', (current_views, clip_id))
            cursor.execute('INSERT INTO user_views (user_id, clip_id) VALUES (?, ?)', (user_id, clip_id))
            conn.commit()
    
    conn.close()
    return current_views

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
    caption = (
        "❤️ **Welcome to All Max Content Bot!** ❤️\n\n"
        "✨ Aapka yahan swagat hai! Niche diye gaye files mein se apna pasandida option select karein:\n"
    )
    current_photo = DYNAMIC_STORAGE["welcome_photo"]
    
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

def get_main_menu_keyboard():
    keyboard = []
    for key, pkg in PACKAGES.items():
        keyboard.append([InlineKeyboardButton(f"{pkg['name']} 🌟 ─── Rs.{pkg['price']}", callback_data=key)])
    
    keyboard.append([InlineKeyboardButton("✨ ── 𝑾𝑨𝑻𝑪𝑯 𝑫𝑬𝑴𝑶 𝑵𝑶𝑾 ── ✨", callback_data="demo_1")])
    keyboard.append([InlineKeyboardButton("🆘 ── 𝒉𝒆𝒍𝒑 & 𝒔𝒖𝒑𝒑𝒐𝒓𝒕 ── 💬", url=SUPPORT_LINK)])
    
    return InlineKeyboardMarkup(keyboard)

async def process_photo_setting(update: Update, context):
    if not update.message.photo:
        await update.message.reply_text("⚠️ Kripya photo ke sath `/setphoto` likhein.")
        return

    photo_file = update.message.photo[-1].file_id
    DYNAMIC_STORAGE["welcome_photo"] = photo_file

    await update.message.reply_text(
        f"✅ **Welcome (Main Menu) ki photo update ho gayi hai!**\n\n"
        f"📋 **Is File ID ko copy karke code mein `DEFAULT_PHOTO` par daal sakte hain:**\n\n`{photo_file}`",
        parse_Markdown="Markdown"
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
        index = int(data.replace("demo_", ""))
        current_views = check_and_increment_view(user_id, index)
        
        nav_buttons = []
        row = []
        if index > 1:
            row.append(InlineKeyboardButton("⬅️ Back", callback_data=f"demo_{index - 1}"))
        if index < 10:
            row.append(InlineKeyboardButton("➡️ Next Clip", callback_data=f"demo_{index + 1}"))
            
        if row:
            nav_buttons.append(row)
            
        nav_buttons.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
        nav_buttons.append([InlineKeyboardButton(PERMANENT_BUTTON_NAME, url=PERMANENT_CHANNEL_LINK)])
        
        keyboard = InlineKeyboardMarkup(nav_buttons)
        
        text = (
            f"🎬 **Demo Clip {index} / 10**\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"✨ Yeh hamari demo clip number {index} hai. Quality check karein!\n\n"
            f"👁️ Views: **{current_views:,}**"
        )
        
        try:
            await query.message.delete()
        except Exception:
            pass
            
        video_file_id = PERMANENT_VIDEOS.get(index)
        current_photo = DYNAMIC_STORAGE["welcome_photo"]
        
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
                caption=text + f"\n\n*(Yeh video abhi upload nahi ki gayi hai.)*",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        context.user_data['last_pkg'] = data
        pkg_photo = pkg["photo"]
        
        text = (
            "🔥💎 **SELECTED VIP FILE** 💎🔥\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"📦 **{pkg['name']}**\n"
            f"💰 Price: **Rs.{pkg['price']}**\n\n"
            "✨ **Payment karne ke liye niche diye gaye button par click karein:** 👇"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Pay Now (UPI QR)", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ])
        
        try:
            await query.message.delete()
        except Exception:
            pass
            
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=pkg_photo,
            caption=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    elif data.startswith("pay_"):
        file_key = data.replace("pay_", "")
        pkg = PACKAGES[file_key]
        context.user_data['last_pkg'] = file_key
        
        try:
            qr_file_path = generate_upi_qr(pkg["price"], pkg["name"], user_id)
            caption = (
                "🚨📱 **SCAN & PAY INSTRUCTIONS** 📱🚨\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                f"📦 **{pkg['name']}**\n"
                f"💰 Price: **Rs.{pkg['price']}**\n\n"
                f"1️⃣ Is QR Code ko scan karke **Rs.{pkg['price']}** pay karein (`{UPI_ID}`).\n"
                f"2️⃣ Payment karne ke baad is chat mein **Payment ka Screenshot** bhejien taaki aapko turant link mil sake."
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

async def handle_media(update: Update, context):
    caption_text = (update.message.caption or "").lower()
    
    if update.message.photo:
        if "setphoto" in caption_text or not caption_text:
            await process_photo_setting(update, context)
            return

    last_file_key = context.user_data.get('last_pkg', 'file_1')
    pkg = PACKAGES.get(last_file_key, PACKAGES['file_1'])

    text = (
        "📸 **Screenshot Received Successfully!**\n\n"
        f"🎉 File: **{pkg['name']}**\n"
        "✨ Aapka payment screenshot mil gaya hai. Niche diye gaye button se apna VIP Access link kholen:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Access VIP Content Link", url=pkg["link"])],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setphoto", process_photo_setting))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT, handle_media))

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
            
