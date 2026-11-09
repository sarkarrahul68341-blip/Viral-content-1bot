import os
import logging
from flask import Flask, send_file
from threading import Thread

# Flask web server setup (Yeh website chalane ke liye hai)
app = Flask(__name__)

@app.route('/')
def home():
    # Yeh root URL par seedha aapka pricing page (index.html) dikhayega
    try:
        return send_file('index.html')
    except Exception as e:
        return "Telegram Bot Server is Running with Single-Message UI Update!"

def run_web_server():
    # Render ke liye port 10000 par server start karega
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()

# --- Yahan se aapka Telegram bot ka main code shuru hota hai ---
# Aapka baaki bot logic, handlers, aur polling yahan aayegi

if __name__ == '__main__':
    # Server ko background mein live rakhne ke liye keep_alive call kiya hai
    keep_alive()
    
    print("Bot and Web Server are starting...")
    # Agar aapka bot polling method use kar raha hai toh yahan bot.infinity_polling() ya jo bhi code ho wo daal dein.
    
