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

# In-memory storage for bot systems
bot_data = {
    "upi_id": "Puja6489@ptyes",
    "balance": 100.0,
    "referral_count": 0,
    "custom_posts": ["📢 Yeh hamara pehla sample post hai!"],
    "buttons_list": ["View Photo", "Watch Video", "Listen Audio"]
}

# ----------------- FLASK SERVER (For Render Keep-Alive) -----------------
app = Flask('')

@app.route('/')
def home():
    return "Advanced Bot is fully alive and running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ----------------- TELEGRAM BOT INTERFACE -----------------

@bot.message_handler(commands=['start'])
def send_main_menu(message):
    show_main_menu(message.chat.id, message.message_id, is_new=True)

def show_main_menu(chat_id, message_id=None, is_new=False):
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
    
    # Text without extra lines
    text = "👋 **Welcome to your Advanced Control Panel!**"
    
    if is_new:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    if call.data == "buttons_editor":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("➕ Add New Button", callback_data="add_button"),
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu")
        )
        btn_text = "🎛️ **Buttons Editor**\nActive Buttons:\n" + "\n".join([f"• {b}" for b in bot_data["buttons_list"]])
        bot.edit_message_text(btn_text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_button":
        msg = bot.send_message(chat_id, "Naye button ka naam bhejein:")
        bot.register_next_step_handler(msg, save_new_button)

    elif call.data == "posts_editor":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("➕ Create New Post", callback_data="create_post"),
            types.InlineKeyboardButton("📄 View Posts", callback_data="view_posts"),
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu")
        )
        bot.edit_message_text("📝 **Posts Editor**", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "create_post":
        msg = bot.send_message(chat_id, "Apne naye post ka text/content yahan bhejein:")
        bot.register_next_step_handler(msg, save_new_post)

    elif call.data == "view_posts":
        posts_text = "📄 **Saved Posts:**\n\n" + "\n---\n".join(bot_data["custom_posts"])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="posts_editor"))
        bot.edit_message_text(posts_text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "balance_menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("💳 Add Funds via UPI", callback_data="get_qr"),
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu")
        )
        bot.edit_message_text(f"💵 **Your Wallet Balance**\nCurrent Balance: ₹{bot_data['balance']}", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "ads_menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text("🏷️ **Advertisement System**", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "extensions_menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text("🧩 **Extensions**", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "referral_menu":
        ref_link = f"https://t.me/{bot.get_me().username}?start=ref_{call.from_user.id}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(f"👣 **Referral System**\nTotal Referrals: {bot_data['referral_count']}\n\nAapka Referral Link:\n`{ref_link}`", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "get_qr":
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
        
        bot.send_photo(chat_id, bio, caption=f"💸 **Autopayments / UPI QR**\nScan karke payment karein.\nUPI ID: `{bot_data['upi_id']}`", parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✏️ Change UPI ID", callback_data="set_upi"),
            types.InlineKeyboardButton("📢 Broadcast Message", callback_data="broadcast_msg"),
            types.InlineKeyboardButton("🔙 Back", callback_data="main_menu")
        )
        bot.edit_message_text("🔐 **Admin Control Panel**", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "set_upi":
        msg = bot.send_message(chat_id, "Kripya apni nayi UPI ID bhejein:")
        bot.register_next_step_handler(msg, save_new_upi)

    elif call.data == "broadcast_msg":
        msg = bot.send_message(chat_id, "Jo message sabhi users ko bhejna hai, woh yahan type karein:")
        bot.register_next_step_handler(msg, process_broadcast)

    elif call.data == "main_menu":
        show_main_menu(chat_id, msg_id)

def save_new_button(message):
    btn_name = message.text.strip()
    bot_data["buttons_list"].append(btn_name)
    bot.send_message(message.chat.id, f"✅ Naya button add ho gaya: `{btn_name}`", parse_mode="Markdown")

def save_new_post(message):
    post_text = message.text.strip()
    bot_data["custom_posts"].append(post_text)
    bot.send_message(message.chat.id, "✅ Naya post save ho gaya hai!", parse_mode="Markdown")

def save_new_upi(message):
    new_upi = message.text.strip()
    bot_data["upi_id"] = new_upi
    bot.send_message(message.chat.id, f"✅ UPI ID update ho gayi hai:\n`{new_upi}`", parse_mode="Markdown")

def process_broadcast(message):
    broadcast_text = message.text.strip()
    bot.send_message(message.chat.id, f"📢 Broadcast Success:\n\n{broadcast_text}")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
