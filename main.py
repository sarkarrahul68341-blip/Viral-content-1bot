import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Render environment variable se bot token uthayega
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# /start command ka handler (Menu buttons ke sath)
@bot.message_handler(commands=['start'])
def main_menu(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    
    # Buttons jo user ko dikhenge
    markup.add(
        InlineKeyboardButton("🎬 Video Catalog dekhein", callback_data='browse_videos'),
        InlineKeyboardButton("💳 Payment kaise karein?", callback_data='help_payment'),
        InlineKeyboardButton("📞 Support / Contact", url='https://t.me/your_username')
    )
    
    welcome_text = (
        "👋 Namaste! Hamare Digital Video Store mein aapka swagat hai.\n\n"
        "Yahan aapko premium videos milengi. Neeche diye gaye button par click karke aage badhein:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Button clicks ko handle karne ke liye
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'browse_videos':
        video_markup = InlineKeyboardMarkup()
        video_markup.add(
            InlineKeyboardButton("🔥 Video 1 (Sample) - ₹99", callback_data='buy_video_1'),
            InlineKeyboardButton("🔙 Main Menu par jayein", callback_data='main_menu')
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📁 Yeh rahi aapki available videos ki list. Kisi ek ko select karein:",
            reply_markup=video_markup
        )
        
    elif call.data == 'buy_video_1':
        payment_text = (
            "📱 **Video 1 Purchase karne ke liye:**\n\n"
            "Aap diye gaye UPI ID par ₹99 bhej sakte hain:\n"
            "`your-upi-id@oksbi`\n\n"
            "Payment karne ke baad uska screenshot ya transaction ID yahan bhej dein, "
            "fir aapko turant video mil jayegi!"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=payment_text,
            parse_mode='Markdown'
        )
        
    elif call.data == 'help_payment':
        bot.answer_callback_query(call.id, "Payment karne ke liye UPI ya QR code ka use karein.")
        
    elif call.data == 'main_menu':
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            InlineKeyboardButton("🎬 Video Catalog dekhein", callback_data='browse_videos'),
            InlineKeyboardButton("💳 Payment kaise karein?", callback_data='help_payment'),
            InlineKeyboardButton("📞 Support / Contact", url='https://t.me/your_username')
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="👋 Main Menu:",
            reply_markup=markup
        )

# Bot ko chalu rakhne ke liye
if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
