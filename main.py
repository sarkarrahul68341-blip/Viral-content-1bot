import os
import threading
import telebot
from telebot import types
import qrcode
from flask import Flask

# Bot Token environment variable se uthayega
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
  raise ValueError("BOT_TOKEN environment variable set nahi hai!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# /start command par menu buttons bhejne ke liye
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.InlineKeyboardMarkup(row_width=2)

  # Menu Inline Buttons
  btn_photo = types.InlineKeyboardButton(
      '📸 Photo Dekhein', callback_data='send_photo'
  )
  btn_video = types.InlineKeyboardButton(
      '🎥 Video Dekhein', callback_data='send_video'
  )
  btn_audio = types.InlineKeyboardButton(
      '🎵 Audio sunein', callback_data='send_audio'
  )
  btn_qr = types.InlineKeyboardButton(
      '💳 UPI QR Code', callback_data='send_qr'
  )

  markup.add(btn_photo, btn_video, btn_audio, btn_qr)

  bot.send_message(
      message.chat.id,
      '👋 Namaste! "All max content" bot mein aapka swagat hai.\n\nNeeche'
      ' diye gaye menu options mein se kisi par bhi click karein:',
      reply_markup=markup,
  )


# Buttons ke click hone par kya response aayega uska code
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
  try:
    if call.data == 'send_photo':
      bot.send_photo(
          call.message.chat.id,
          'https://picsum.photos/400/300',
          caption='📸 Yeh lijiye aapki sample photo!',
      )

    elif call.data == 'send_video':
      bot.send_message(
          call.message.chat.id,
          '🎥 Yeh lijiye sample video:\nhttps://www.w3schools.com/html/mov_bbb.mp4',
      )

    elif call.message and call.data == 'send_audio':
      bot.send_message(
          call.message.chat.id,
          '🎵 Audio feature active hai! Aap yahan apni pasand ki audio file set'
          ' kar sakte hain.',
      )

    elif call.data == 'send_qr':
      # Yahan apni asli UPI ID daal dein
      upi_id = 'apki_upi_id@paytm'
      name = 'All Max Content'
      upi_url = f'upi://pay?pa={upi_id}&pn={name}&cu=INR'

      img = qrcode.make(upi_url)
      qr_path = 'upi_qr.png'
      img.save(qr_path)

      with open(qr_path, 'rb') as photo:
        bot.send_photo(
            call.message.chat.id,
            photo,
            caption=(
                '💳 Yeh lijiye aapka UPI QR code! Is par scan karke payment ki'
                ' ja sakti hai.'
            ),
        )

      if os.path.exists(qr_path):
        os.remove(qr_path)

    bot.answer_callback_query(call.id)
  except Exception as e:
    print(f'Error in callback: {e}')


# Render ke liye Flask Web Server route
@app.route('/')
def home():
  return 'Bot is running successfully with all options!'


def run_bot():
  # Bot polling ko background thread mein lagataar chalane ke liye
  bot.infinity_polling(skip_pending=True)


if __name__ == '__main__':
  # Bot polling ko alag thread mein start karna
  t = threading.Thread(target=run_bot)
  t.daemon = True
  t.start()

  # Flask server ko run karna (Render ke port par)
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)
