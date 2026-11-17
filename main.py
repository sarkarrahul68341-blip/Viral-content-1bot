import os
import asyncio
import sqlite3
import re
import shlex
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

# Permanent Channel Link (jo Back to Main Menu ke niche dikhega)
PERMANENT_CHANNEL_LINK = "https://t.me/+w4MJrYfZ2zlyMTQ1"
PERMANENT_BUTTON_NAME = "🔥 Join Our Channel"

# Default welcome photo
DEFAULT_PHOTO = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# ==================== DATABASE SETUP ====================
def init_db():
    try:
        conn = sqlite3.connect('bot_views.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demo_stats (
                clip_id INTEGER PRIMARY KEY,
                video_file_id TEXT,
                views INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demo_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clip_id INTEGER,
                button_name TEXT,
                link_url TEXT
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
    except Exception as e:
        print(f"DB Init Error: {e}")

init_db()

def get_clip_data(clip_id):
    try:
        conn = sqlite3.connect('bot_views.db')
        cursor = conn.cursor()
        cursor.execute('SELECT video_file_id, views FROM demo_stats WHERE clip_id = ?', (clip_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"Get Clip Error: {e}")
        return None

def get_clip_links(clip_id):
    try:
        conn = sqlite3.connect('bot_views.db')
        cursor = conn.cursor()
        cursor.execute('SELECT button_name, link_url FROM demo_links WHERE clip_id = ?', (clip_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows 
    except Exception as e:
        print(f"Get Links Error: {e}")
        return []

def add_clip_link(clip_id, button_name, link):
    try:
        conn = sqlite3.connect('bot_views.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO demo_links (clip_id, button_name, link_url) VALUES (?, ?, ?)', (clip_id, button_name, link))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Add Link Error: {e}")

def clear_clip_links(clip_id):
    try:
        conn = sqlite3.connect('bot_views.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM demo_links WHERE clip_id = ?', (clip_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Clear Links Error: {e}")

def check_and_increment_view(user_id, clip_id):
    try:
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
    except Exception as e:
        print(f"View Increment Error: {e}")
        return 0

def save_video_to_db(clip_id, file_id):
    try:
        conn = sqlite3.connect('bot_views.db')
        cursor = conn.cursor()
        cursor.execute('SELECT views FROM demo_stats WHERE clip_id = ?', (clip_id,))
        row = cursor.fetchone()
        initial_views = row[0] if row else 0
        
        cursor.execute('''
            INSERT INTO demo_stats (clip_id, video_file_id, views) 
            VALUES (?, ?, ?) 
            ON CONFLICT(clip_id) DO UPDATE SET video_file_id = excluded.video_file_id
        ''', (clip_id, file_id, initial_views))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Save Video Error: {e}")

# ==================== 8 FILES CONFIGURATION ====================
PACKAGES = {
    "file_1": {"name": "⭐ 01 All mix content VIP Access", "price": 249, "link": "https://t.me/+s4Zzmwni59diNjU1", "photo": DEFAULT_PHOTO},
    "file_2": {"name": "🔑 02 Rap & Big File VD", "price": 89, "link": "https://t.me/+_AILkUGhVnVkMzBl", "photo": DEFAULT_PHOTO},
    "file_3": {"name": "🔑 03 Mom and Son Real Sex", "price": 45, "link": "https://t.me/+qjTxEmHC-z4wMzE1", "photo": DEFAULT_PHOTO},
    "file_4": {"name": "🔞 04 Insta viral reels and sex", "price": 40, "link": "https://t.me/+LmzeU14SK_I0MGY9", "photo": DEFAULT_PHOTO},
    "file_5": {"name": "🔥 05 Ganga bath group join", "price": 199, "link": "https://t.me/+jMs1EZ3RLSc1Yjhl", "photo": DEFAULT_PHOTO},
    "file_6": {"name": "🔥 06 Bath camera hidden", "price": 55, "link": "https://t.me/+G4yBWASYMzYzOTc9", "photo": DEFAULT_PHOTO},
    "file_7": {"name": "🔥 07 CP girl real fuke", "price": 65, "link": "https://t.me/+f9i3BlsoUeZiZmY1", "photo": DEFAULT_PHOTO},
    "file_8": {"name": "❤️ 08 Sister and brother sex", "price": 30, "link": "https://t.me/+BYOIdmg4w3c2MjQ1", "photo": DEFAULT_PHOTO},
}

def get_main_menu_keyboard():
    keyboard = []
    for key, pkg in PACKAGES.items():
        keyboard.append([InlineKeyboardButton(f"{pkg['name']} 🌟 ─── Rs.{pkg['price']}", callback_data=key)])
    
    keyboard.append([InlineKeyboardButton("✨ ── 𝑾𝑨𝑻𝑪𝑯 𝑫𝑬𝑴𝑶 𝑵𝑶𝑾 ── ✨", callback_data="demo_1")])
    keyboard.append([InlineKeyboardButton("🆘 ── 𝒉𝒆𝒍𝒑 & 𝒔𝒖𝒑𝒑𝒐𝒓𝒕 ── 💬", url=SUPPORT_LINK)])
    
    return InlineKeyboardMarkup(keyboard)

def generate_upi_qr(amount, pkg_name, order_id):
    try:
        upi_uri = f"upi://pay?pa={UPI_ID}&pn={BUSINESS_NAME}&am={amount}&cu=INR&tn=Order_{order_id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(upi_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        filename = f"qr_{order_id}.png"
        img.save(filename)
        return filename
    except Exception as e:
        print(f"QR Gen Error: {e}")
        return None

# ==================== HANDLERS ====================
async def start(update: Update, context):
    try:
        reply_markup = get_main_menu_keyboard()
        caption = (
            "❤️ **Welcome to All Max Content Bot!** ❤️\n\n"
            "✨ Aapka yahan swagat hai! Niche diye gaye files mein se apna pasandida option select karein:\n"
        )
        
        if update.callback_query:
            query = update.callback_query
            try:
                await query.message.delete()
            except Exception:
                pass
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=DEFAULT_PHOTO,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_photo(
                photo=DEFAULT_PHOTO,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
    except Exception as e:
        print(f"Start Error: {e}")

async def process_photo_setting(update: Update, context):
    try:
        global DEFAULT_PHOTO
        if not update.message.photo:
            await update.message.reply_text("⚠️ Kripya photo ke sath command likhein.")
            return

        photo_file = update.message.photo[-1].file_id
        caption_text = (update.message.caption or "").strip().lower()

        file_key = None
        numbers = re.findall(r'\d+', caption_text)
        
        if numbers:
            num = int(numbers[0])
            if 1 <= num <= 8:
                file_key = f"file_{num}"

        for key in PACKAGES.keys():
            if key in caption_text or key.replace("_", "") in caption_text.replace("_", ""):
                file_key = key
                break

        if file_key and file_key in PACKAGES:
            PACKAGES[file_key]["photo"] = photo_file
            await update.message.reply_text(f"✅ **{PACKAGES[file_key]['name']}** ki alag photo successfully update ho gayi hai!")
        else:
            DEFAULT_PHOTO = photo_file
            await update.message.reply_text("✅ **Main Menu (Welcome)** ki photo successfully update ho gayi hai!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def process_video_setting(update: Update, context):
    try:
        if not update.message.video:
            await update.message.reply_text("⚠️ Kripya video ke sath command likhein, jaise: `/setdemo 2`", parse_mode="Markdown")
            return

        video_file_id = update.message.video.file_id
        caption_text = (update.message.caption or "").strip()
        
        numbers = re.findall(r'\d+', caption_text)
        clip_num = 1
        if numbers:
            clip_num = int(numbers[-1])

        if 1 <= clip_num <= 10:
            save_video_to_db(clip_num, video_file_id)
            await update.message.reply_text(f"✅ **Demo Clip {clip_num} / 10** successfully save ho gayi hai!")
        else:
            await update.message.reply_text("⚠️ Kripya 1 se 10 ke beech ka number dein (jaise `/setdemo 2`).")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def add_demo_link_handler(update: Update, context):
    try:
        text = update.message.text or ""
        try:
            parts = shlex.split(text)
        except Exception:
            parts = text.split()
        
        if len(parts) >= 4:
            clip_num_str = parts[1]
            button_name = parts[2]
            link = parts[3]
        elif context.args and len(context.args) >= 3:
            clip_num_str = context.args[0]
            button_name = context.args[1]
            link = context.args[2]
        else:
            await update.message.reply_text("⚠️ Sahi tarika: `/adddemolink 1 \"🔥 Join Channel\" https://t.me/your_link`", parse_mode="Markdown")
            return
        
        if not clip_num_str.isdigit() or not (1 <= int(clip_num_str) <= 10):
            await update.message.reply_text("⚠️ Kripya 1 se 10 ke beech ka clip number dein.")
            return
            
        clip_num = int(clip_num_str)
        add_clip_link(clip_num, button_name, link)
        await update.message.reply_text(f"✅ **Demo Clip {clip_num}** mein naya button add ho gaya hai!\n🏷️ Name: `{button_name}`\n🔗 Link: `{link}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error adding link: {str(e)}")

async def clear_demo_links_handler(update: Update, context):
    try:
        text = update.message.text or ""
        parts = text.split()
        
        if context.args and len(context.args) >= 1:
            clip_num_str = context.args[0]
        elif len(parts) >= 2:
            clip_num_str = parts[1]
        else:
            await update.message.reply_text("⚠️ Sahi tarika: `/cleardemolinks 1`", parse_mode="Markdown")
            return
        
        if not clip_num_str.isdigit() or not (1 <= int(clip_num_str) <= 10):
            await update.message.reply_text("⚠️ Kripya 1 se 10 ke beech ka clip number dein.")
            return
            
        clip_num = int(clip_num_str)
        clear_clip_links(clip_num)
        await update.message.reply_text(f"✅ **Demo Clip {clip_num}** ke saare custom links clear kar diye gaye hain.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error clearing links: {str(e)}")

async def button_handler(update: Update, context):
    try:
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
            clip_data = get_clip_data(index)
            video_file_id = clip_data[0] if clip_data else None
            custom_links = get_clip_links(index) 
            
            nav_buttons = []
            
            # Additional custom links added via /adddemolink
            for btn_name, link_url in custom_links:
                nav_buttons.append([InlineKeyboardButton(btn_name, url=link_url)])
            
            row = []
            if index > 1:
                row.append(InlineKeyboardButton("⬅️ Back", callback_data=f"demo_{index - 1}"))
            if index < 10:
                row.append(InlineKeyboardButton("➡️ Next Clip", callback_data=f"demo_{index + 1}"))
                
            if row:
                nav_buttons.append(row)
                
            # Back to Main Menu button
            nav_buttons.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
            
            # Permanent Channel Button right below Back to Main Menu
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
                    photo=DEFAULT_PHOTO,
                    caption=text + f"\n\n*(Yeh video abhi upload nahi ki gayi hai. /setdemo {index} use karein)*",
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            return

        if data in PACKAGES:
            pkg = PACKAGES[data]
            context.user_data['last_pkg'] = data
            
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
                photo=pkg["photo"],
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
                if qr_file_path and os.path.exists(qr_file_path):
                    os.remove(qr_file_path)
            except Exception as e:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"❌ Error generating QR code: {str(e)}"
                )
    except Exception as e:
        print(f"Button Handler Error: {e}")

async def handle_media(update: Update, context):
    try:
        caption_text = (update.message.caption or "").lower()
        
        if update.message.video and "setdemo" in caption_text:
            await process_video_setting(update, context)
            return
            
        if update.message.photo and ("setphoto" in caption_text or "file" in caption_text or any(f"file_{i}" in caption_text or f" {i} " in f" {caption_text} " for i in range(1, 9))):
            await process_photo_setting(update, context)
            return
        elif update.message.photo and not caption_text:
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
            [InlineKeyboardButton("🔗 Access VIP Content Link", url=p
