import os
import telebot
from telebot import types
import qrcode
from io import BytesIO
from flask import Flask
from threading import Thread

# Bot Token (Render environment variable se uthayega)
TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = telebot.TeleBot(TOKEN)

# Aapki Admin Telegram User ID
ADMIN_ID = 0  # Aap baad mein apni numeric ID yahan daal sakti hain

# Dynamic Content & Settings (Aapki UPI ID ke sath)
bot_data = {
    "upi_id": "Puja6489@ptyes",
    "photo_caption": "📸 Yeh lijiye aapki requested photo!",
    "photo_url": "https://picsum.photos/400/300",
    "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
}

# ----------------- FLASK SERVER (Render ke liye) -----------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ----------------- TELEGRAM BOT LOGIC -----------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Colorful & Attractive Buttons
    btn_photo = types.InlineKeyboardButton("📸 View Photo", callback_data="get_photo")
    btn_video = types.InlineKeyboardButton("🎥 Watch Video", callback_data="get_video")
    btn_audio = types.InlineKeyboardButton("🎵 Listen Audio", callback_data="get_audio")
    btn_qr = types.InlineKeyboardButton("💳 Pay via UPI QR", callback_data="get_qr")
    
    markup.add(btn_photo, btn_video, btn_audio, btn_qr)
    
    # Admin Panel Button
    btn_admin = types.InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")
    markup.add(btn_admin)

    welcome_text = (
        "👋 **Welcome to the Content Bot!**\n\n"
        "Neeche diye gaye buttons par click karke content access karein:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    if call.data == "get_photo":
        bot.send_photo(chat_id, bot_data["photo_url"], caption=bot_data["photo_caption"])
        
    elif call.data == "get_video":
        bot.send_video(chat_id, bot_data["video_url"], caption="🎥 Yeh lijiye aapka video!")
        
    elif call.data == "get_audio":
        bot.send_audio(chat_id, bot_data["audio_url"], caption="🎵 Yeh lijiye aapka audio!")
        
    elif call.data == "get_qr":
        # Generate UPI QR Code dynamically based on Puja6489@ptyes
        upi_string = f"upi://pay?pa={bot_data['upi_id']}&pn=Store&cu=INR"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(upi_string)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        bio = BytesIO()
        bio.name = 'upi_qr.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        bot.send_photo(chat_id, bio, caption=f"💳 Scan & Pay via UPI\nUPI ID: `{bot_data['upi_id']}`", parse_mode="Markdown")

    elif call.data == "admin_panel":
        admin_markup = types.InlineKeyboardMarkup(row_width=1)
        admin_markup.add(
            types.InlineKeyboardButton("✏️ Change UPI ID", callback_data="set_upi"),
            types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
        )
        bot.edit_message_text("⚙️ **Admin Panel**\nAap yahan se bot ki settings change kar sakti hain:", 
                              chat_id=chat_id, message_id=call.message.message_id, reply_markup=admin_markup, parse_mode="Markdown")

    elif call.data == "set_upi":
        msg = bot.send_message(chat_id, "Kripya apni nayi UPI ID bhejein (jaise: `yourname@paytm`):")
        bot.register_next_step_handler(msg, save_new_upi)

    elif call.data == "main_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📸 View Photo", callback_data="get_photo"),
            types.InlineKeyboardButton("🎥 Watch Video", callback_data="get_video"),
            types.InlineKeyboardButton("🎵 Listen Audio", callback_data="get_audio"),
            types.InlineKeyboardButton("💳 Pay via UPI QR", callback_data="get_qr"),
            types.InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")
        )
        bot.edit_message_text("👋 **Main Menu:**", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

def save_new_upi(message):
    new_upi = message.text.strip()
    bot_data["upi_id"] = new_upi
    bot.send_message(message.chat.id, f"✅ UPI ID successfully update ho gayi hai:\n`{new_upi}`", parse_mode="Markdown")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
