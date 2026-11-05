import os
from flask import Flask
from threading import Thread
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

# ================= CONFIGURATION & SETTINGS =================
BOT_TOKEN = "9094967544:AAHiB3IEVow4A5JRl4BIdt4HijZwHYR_qE4"
ADMIN_ID = 8776203848  # Aapki personal Telegram User ID

# Runtime storage for dynamic editing via admin panel
bot_data = {
    "welcome_message": "Hello everyone ❤️\n\nWelcome to our official digital store! Niche diye gaye buttons se select karein:",
    "upi_id": "apka-upi-id@okhdfcbank",
    "products": {
        "item_1": {"title": "🎬 Premium Video Pack", "price": "₹199", "file_url": "https://example.com/video.mp4"}
    }
}

user_state = {}
# ============================================================

bot = telebot.TeleBot(BOT_TOKEN)

# Flask Keep-Alive Server for Render (24/7 uptime)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- KEYBOARDS ---
def get_main_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🎛️ Buttons Editor"), KeyboardButton("📝 Posts Editor"),
        KeyboardButton("💰 Balance"), KeyboardButton("📣 Advertisement"),
        KeyboardButton("🧩 Extensions"), KeyboardButton("📈 Referral System"),
        KeyboardButton("💳 Autopayments"), KeyboardButton("🔐 Admin")
    )
    return markup

def get_admin_sub_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📥 Mailing"), KeyboardButton("📊 Statistics"),
        KeyboardButton("📣 Advertisement"), KeyboardButton("🍀 Extensions"),
        KeyboardButton("📋 Variables"), KeyboardButton("⚙️ Bot Settings"),
        KeyboardButton("🔠 Pagination"), KeyboardButton("📈 Referral System"),
        KeyboardButton("💬 Message for START"), KeyboardButton("📢 Channels & Groups"),
        KeyboardButton("💳 Autopayments"), KeyboardButton("👥 Manage Admins"),
        KeyboardButton("🤖 Secretary Bot"), KeyboardButton("🛒 Shop"),
        KeyboardButton("⬅️ Exit Admin")
    )
    return markup

def get_buttons_editor_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("➕ Add Button"))
    markup.add(KeyboardButton("🛑 Stop Editor"), KeyboardButton("📝 Posts Editor"))
    return markup

def get_cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton("🚫 Cancel"))
    return markup

# /start command
@bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🛠️ **Admin Panel Opened**", reply_markup=get_main_admin_keyboard(), parse_mode="Markdown")
        return

    kb = InlineKeyboardMarkup(row_width=1)
    for key, item in bot_data["products"].items():
        kb.add(InlineKeyboardButton(f"{item['title']} ({item['price']})", callback_data=f"buy_{key}"))
    kb.add(InlineKeyboardButton("📞 Contact Support", url="https://t.me/your_username"))

    bot.send_message(message.chat.id, bot_data["welcome_message"], reply_markup=kb, parse_mode="Markdown")

# /admin command
@bot.message_handler(commands=['admin'])
def admin_panel_cmd(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🔧 **You are in the Administrator menu.**", reply_markup=get_main_admin_keyboard(), parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ You are not authorized!")

# --- ADMIN PANEL ACTIONS & SUB-MENU HANDLER ---
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID)
def admin_menu_actions(message):
    text = message.text
    chat_id = message.chat.id

    if text == "🚫 Cancel":
        user_state.pop(chat_id, None)
        bot.send_message(chat_id, "❌ Cancelled. Back to Main Admin Menu:", reply_markup=get_main_admin_keyboard())

    elif text == "🎛️ Buttons Editor":
        bot.send_message(chat_id, "🎛️ **You are in Button Editing mode.**", reply_markup=get_buttons_editor_keyboard(), parse_mode="Markdown")

    elif text == "➕ Add Button":
        user_state[chat_id] = "waiting_for_button_name"
        msg = (
            "➕ **Adding new button.**\n\n"
            "✨ Enter a Name for the new button.\n\n"
            "Press «🚫 Cancel» if you change your mind."
        )
        bot.send_message(chat_id, msg, reply_markup=get_cancel_keyboard(), parse_mode="Markdown")

    elif text == "🛑 Stop Editor":
        bot.send_message(chat_id, "🛑 Editor stopped. Back to Admin Menu:", reply_markup=get_main_admin_keyboard())

    elif text == "📝 Posts Editor" or text == "💬 Message for START":
        user_state[chat_id] = "waiting_for_start_msg"
        bot.send_message(chat_id, "✍️ Naya Welcome/Start message yahan bhej dein:", reply_markup=get_cancel_keyboard())

    elif text == "💰 Balance":
        bot.send_message(chat_id, "💰 **Bot Balance Overview:**\nCurrent Wallet Balance: ₹0.00\nTotal Revenue: ₹0.00", reply_markup=get_main_admin_keyboard(), parse_mode="Markdown")

    elif text == "📣 Advertisement":
        bot.send_message(chat_id, "📣 **Broadcast & Advertisement:** Users ko promotional message bhejne ke liye text type karein.", reply_markup=get_main_admin_keyboard())

    elif text == "🧩 Extensions" or text == "🍀 Extensions":
        bot.send_message(chat_id, "🧩 **Extensions Panel:** Additional bot plugins aur features yahan manage hote hain.", reply_markup=get_main_admin_keyboard(), parse_mode="Markdown")

    elif text == "📈 Referral System" or text == "👥 Ref. System":
        bot.send_message(chat_id, "📈 **Referral System:** Total referred users: 0", reply_markup=get_main_admin_keyboard(), parse_mode="Markdown")

    elif text == "💳 Autopayments":
        user_state[chat_id] = "waiting_for_upi"
        bot.send_message(chat_id, f"💳 Apni nayi UPI ID bhejein (Current: `{bot_data['upi_id']}`):", parse_mode="Markdown", reply_markup=get_cancel_keyboard())

    elif text == "🔐 Admin":
        bot.send_message(chat_id, "🔧 **Advanced Administrator Sub-Menu:**", reply_markup=get_admin_sub_keyboard(), parse_mode="Markdown")

    elif text == "📊 Statistics":
        bot.send_message(chat_id, "📊 **Bot Statistics:**\nTotal Users: 1\nActive Orders: 0", reply_markup=get_admin_sub_keyboard(), parse_mode="Markdown")

    elif text == "🛒 Shop":
        shop_info = "🛒 **Current Shop Items:**\n"
        for k, v in bot_data["products"].items():
            shop_info += f"- {v['title']} | {v['price']}\n"
        bot.send_message(chat_id, shop_info, reply_markup=get_admin_sub_keyboard(), parse_mode="Markdown")

    elif text == "👥 Manage Admins":
        bot.send_message(chat_id, f"👥 **Admin User ID:** `{ADMIN_ID}`", parse_mode="Markdown", reply_markup=get_admin_sub_keyboard())

    elif text == "⬅️ Exit Admin" or text == "🔚 Exit Admin":
        bot.send_message(chat_id, "Exited Admin Menu.", reply_markup=get_main_admin_keyboard())

    elif chat_id in user_state:
        state = user_state[chat_id]
        if state == "waiting_for_button_name":
            user_state.pop(chat_id, None)
            bot.send_message(chat_id, f"✅ Button name saved: **{text}**\n\nAb is button ka link ya action URL bhejein:", reply_markup=get_cancel_keyboard(), parse_mode="Markdown")
        elif state == "waiting_for_start_msg":
            bot_data["welcome_message"] = text
            user_state.pop(chat_id, None)
            bot.send_message(chat_id, "✅ Start message update ho gaya!", reply_markup=get_main_admin_keyboard())
        elif state == "waiting_for_upi":
            bot_data["upi_id"] = text
            user_state.pop(chat_id, None)
            bot.send_message(chat_id, f"✅ UPI ID update ho gayi: `{text}`", parse_mode="Markdown", reply_markup=get_main_admin_keyboard())
    else:
        bot.send_message(chat_id, "Kripya menu se koi button select karein.", reply_markup=get_main_admin_keyboard())

# Product purchase handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def process_buy(call):
    item_key = call.data.replace("buy_", "")
    item = bot_data["products"].get(item_key)
    
    if item:
        payment_text = (
            f"🛒 **Product:** {item['title']}\n"
            f"💰 **Price:** {item['price']}\n\n"
            f"📌 **Payment Instructions:**\n"
            f"1. Is UPI ID par payment karein:\n"
            f"   `{bot_data['upi_id']}`\n"
            f"2. Payment ke baad UTR ya screenshot isi chat mein bhej dein."
        )
        bot.send_message(call.message.chat.id, payment_text, parse_mode="Markdown")

# Payment proof handler
@bot.message_handler(content_types=['photo', 'text'])
def handle_payment_proof(message):
    if message.chat.id == ADMIN_ID:
        return

    user_info = f"👤 **User:** @{message.from_user.username} (ID: `{message.chat.id}`)"
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ Approve & Send Content", callback_data=f"approve_{message.chat.id}_item_1"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.chat.id}")
    )

    bot.send_message(ADMIN_ID, f"📩 **New Payment Proof!**\n{user_info}")
    if message.content_type == 'photo':
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    else:
        bot.send_message(ADMIN_ID, f"UTR/Note: {message.text}")
    bot.send_message(ADMIN_ID, "Action lein:", reply_markup=kb)
    bot.reply_to(message, "✅ Payment proof mil gaya hai! Verification ke baad content mil jayega.")

# Admin approval handler
@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def process_admin_action(call):
    data = call.data.split("_")
    action = data[0]
    user_id = int(data[1])

    if action == "approve":
        item = bot_data["products"]["item_1"]
        bot.send_message(user_id, f"🎉 **Payment Verified!**\n\nContent:\n{item['file_url']}", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Delivered!")
        bot.edit_message_text(f"✅ Approved & Delivered to {user_id}", call.message.chat.id, call.message.message_id)
    elif action == "reject":
        bot.send_message(user_id, "❌ Payment verify nahi ho paya. Sahi UTR bhejein.")
        bot.answer_callback_query(call.id, "Rejected.")
        bot.edit_message_text(f"❌ Rejected for {user_id}", call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.remove_webhook()
    bot.infinity_polling()
