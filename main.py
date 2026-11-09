from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Yeh seedha root URL par index.html file serve karega
    return send_file('index.html')

# (Aapka baaki ka Telegram bot ka code yahan niche rahega...)
