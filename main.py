import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot token
TOKEN = '7611593361:AAE2J1tqYk06Vd35h4S5h0aTf8v6Q5J7u4k'
bot = telebot.TeleBot(TOKEN)

# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Namaste! Hamare Digital Video Store mein aapka swagat hai.\n\n"
        "Yahan aapko premium videos milengi. Neeche diye gaye button par click karke aage badhein:"
    )
    
    # Main menu ke buttons
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🎬 Video Catalog dekhein", callback_data='browse_videos'),
        InlineKeyboardButton("💳 Payment kaise karein?", callback_data='help_payment'),
        InlineKeyboardButton("📞 Support / Contact", url='https://t.me/fsipsy')
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Callback queries handler (Buttons ke liye)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'browse_videos':
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔥 Video 1 (Sample) - ₹99", callback_data='buy_video_1'),
            InlineKeyboardButton("🔙 Main Menu par jayein", callback_data='main_menu')
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📂 Yeh rahi hamari available videos ki list. Kisi ek ko select karein:",
            reply_markup=markup
        )
        
    elif call.data == 'help_payment':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Main Menu par jayein", callback_data='main_menu'))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="💳 **Payment Kaise Karein:**\n\n1. Video select karein.\n2. Diye gaye QR code ya UPI ID par payment karein.\n3. Payment ka screenshot Support par bhejein, aapko video mil jayegi.",
            reply_markup=markup,
            parse_mode='Markdown'
        )
        
    elif call.data == 'main_menu':
        welcome_text = (
            "👋 Namaste! Hamare Digital Video Store mein aapka swagat hai.\n\n"
            "Yahan aapko premium videos milengi. Neeche diye gaye button par click karke aage badhein:"
        )
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            InlineKeyboardButton("🎬 Video Catalog dekhein", callback_data='browse_videos'),
            InlineKeyboardButton("💳 Payment kaise karein?", callback_data='help_payment'),
            InlineKeyboardButton("📞 Support / Contact", url='https://t.me/fsipsy')
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=welcome_text,
            reply_markup=markup
        )
        
    elif call.data == 'buy_video_1':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Back to Catalog", callback_data='browse_videos'))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎬 **Video 1 (Sample)**\nPrice: ₹99\n\nPayment karne ke liye hamare Support link par contact karein.",
            reply_markup=markup,
            parse_mode='Markdown'
        )

# Bot ko chalu rakhne ke liye
bot.infinity_polling()
