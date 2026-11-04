import os
import telebot
from telebot import types
import qrcode
from io import BytesIO
from flask import Flask
from threading import Thread

# Bot Token from Environment
TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = telebot.TeleBot(TOKEN)

# User and Bot Data Storage (In-memory for smooth running)
bot_data = {
    "upi_id": "Puja6489@ptyes",
    "balance": 0.0,
    "referral_count": 0,
    "photo_caption": "📸 Yeh lijiye aapka content!",
    "photo_url": "https://picsum.photos/400/300",
    "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
}

# ----------------- FLASK SERVER (For Render Keep-Alive) -----------------
app = Flask('')

@app.route('/')
def home():
    return "Advanced Bot is alive and running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ----------------- TELEGRAM BOT INTERFACE -----------------

@bot.message_handler(commands=['start'])
def send_main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Main Dashboard Buttons matching your layout
    btn_buttons = types.InlineKeyboardButton("🎛️ Buttons Editor", callback_data="buttons_editor")
    btn_posts = types.InlineKeyboardButton("📝 Posts Editor", callback_data="posts_editor")
    btn_balance = types.InlineKeyboardButton("💵 Balance", callback_data="balance_menu")
    btn_ads = types.InlineKeyboardButton("🏷️ Advertisement", callback_data="ads_menu")
    btn_extensions = types.InlineKeyboardButton("🧩 Extensions", callback_data="extensions_menu")
    btn_referral = types.InlineKeyboardButton("👣 Referral System", callback_data="referral_menu")
    btn_autopay = types.InlineKeyboardButton("💸 Autopayments", callback_data="get_qr")
    btn_admin = types.InlineKeyboardButton("🔐 Admin", callback_data="admin_menu")
    
    markup.add(btn_buttons, btn_posts, btn_balance, btn_ads, btn_extensions, btn_referral, btn_autopay, btn_admin)
    
    text = "👋 **Welcome to your Advanced Control Panel!**\n\nNeeche diye gaye options mein se select karein:"
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    
    if call.data == "buttons_editor":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text("🎛️ **Buttons Editor**\nYahan se aap menu buttons ko customize kar sakte hain.", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "posts_editor":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text("📝 **Posts Editor**\nYahan se aap naye posts aur media manage kar sakte hain.", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "balance_menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(f"💵 **Your Balance**\nCurrent Balance: ₹{bot_data['balance']}", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "ads_menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text("🏷️ **Advertisement System**\nPromotional banners aur sponsored messages manage karein.", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "extensions_menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text("🧩 **Extensions**\nAdditional plugins aur features yahan available hain.", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "referral_menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(f"👣 **Referral System**\nTotal Referrals: {bot_data['referral_count']}\nShare your link to earn bonuses!", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "get_qr":
        # Autopayments & UPI QR Generation
        upi_string = f"upi://pay?pa={bot_data['upi_id']}&pn=Store&cu=INR"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(upi_string)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        bio = BytesIO()
        bio.name = 'upi_qr.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        
        bot.send_photo(chat_id, bio, caption=f"💸 **Autopayments / UPI**\nScan to pay securely.\nUPI ID: `{bot_data['upi_id']}`", parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✏️ Change UPI ID", callback_data="set_upi"),
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu")
        )
        bot.edit_message_text("🔐 **Admin Control Panel**\nSelect an action:", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "set_upi":
        msg = bot.send_message(chat_id, "Kripya apni nayi UPI ID bhejein:")
        bot.register_next_step_handler(msg, save_new_upi)

    elif call.data == "main_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🎛️ Buttons Editor", callback_data="buttons_editor"),
            types.InlineKeyboardButton("📝 Posts Editor", callback_data="posts_editor"),
            types.InlineKeyboardButton("💵 Balance", callback_data="balance_menu"),
            types.InlineKeyboardButton("🏷️ Advertisement", callback_data="ads_menu"),
            types.InlineKeyboardButton("🧩 Extensions", callback_data="extensions_menu"),
            types.InlineKeyboardButton("👣 Referral System", callback_data="referral_menu"),
            types.InlineKeyboardButton("💸 Autopayments", callback_data="get_qr"),
            types.InlineKeyboardButton("🔐 Admin", callback_data="admin_menu")
        )
        bot.edit_message_text("👋 **Main Menu:**", chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

def save_new_upi(message):
    new_upi = message.text.strip()
    bot_data["upi_id"] = new_upi
    bot.send_message(message.chat.id, f"✅ UPI ID successfully updated to:\n`{new_upi}`", parse_mode="Markdown")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
