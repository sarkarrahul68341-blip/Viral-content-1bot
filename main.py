import os
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN', '9094967544:AAFkhj5QPoiP2clIBU3JyXAmlrql0YzZam4')
bot = telebot.TeleBot(TOKEN)

# 1. Main Menu (Root Folder)
@bot.message_handler(commands=['start'])
def main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Folders / Categories
    btn_folder1 = types.InlineKeyboardButton("📁 Videos & Demos", callback_data="folder_videos")
    btn_folder2 = types.InlineKeyboardButton("📁 VIP Plans", callback_data="folder_plans")
    btn_support = types.InlineKeyboardButton("💬 Support", callback_data="support")
    
    markup.add(btn_folder1, btn_folder2, btn_support)
    
    text = "📂 **Main Menu (Home Folder)**\n\nNiche diye gaye folders mein se koi ek select karein:"
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# 2. Button Clicks aur Sub-Folders Handling
@bot.callback_query_handler(func=lambda call: True)
def navigate_folders(call):
    
    # Agar user ne "Videos & Demos" folder khola
    if call.data == "folder_videos":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("▶️ Watch Demo 1", callback_data="demo_1"),
            types.InlineKeyboardButton("▶️ Watch Demo 2", callback_data="demo_2"),
            types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_home")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📁 **Videos Folder**\n\nApni pasand ki video select karein:",
            reply_markup=markup,
            parse_mode="Markdown"
        )

    # Agar user ne "VIP Plans" folder khola
    elif call.data == "folder_plans":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💎 Monthly Plan - ₹99", callback_data="plan_month"),
            types.InlineKeyboardButton("👑 Lifetime Plan - ₹499", callback_data="plan_life"),
            types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_home")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📁 **Plans Folder**\n\nAvailable plans yahan hain:",
            reply_markup=markup,
            parse_mode="Markdown"
        )

    # Wapas Main Menu (Home) par jaane ke liye
    elif call.data == "back_home":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📁 Videos & Demos", callback_data="folder_videos"),
            types.InlineKeyboardButton("📁 VIP Plans", callback_data="folder_plans"),
            types.InlineKeyboardButton("💬 Support", callback_data="support")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📂 **Main Menu (Home Folder)**\n\nNiche diye gaye folders mein se koi ek select karein:",
            reply_markup=markup,
            parse_mode="Markdown"
        )

    # Support button action
    elif call.data == "support":
        bot.answer_callback_query(call.id, text="Support section open ho raha hai...")
        bot.send_message(call.message.chat.id, "💬 Contact for help: @your_username")

if __name__ == '__main__':
    bot.infinity_polling()
