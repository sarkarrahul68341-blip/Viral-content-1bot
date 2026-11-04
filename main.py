# Unwanted adult words ki list (Yahan aap apne hisab se words add kar sakte hain)
ADULT_WORDS = ["adult_word1", "adult_word2", "explicit_term"] 

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    user_text = message.text.lower()
    
    # 1. Check karna ki message mein koi adult word hai ya nahi
    if any(word in user_text for word in ADULT_WORDS):
        try:
            # Agar bot ke pas admin rights hain toh galat message ko delete bhi kar sakta hai
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
            
        # User ko warning message bhejna
        bot.send_message(
            message.chat.id, 
            f"⚠️ **Warning @{message.from_user.username or message.from_user.first_name}:**\nAapke message mein inappropriate content paya gaya hai. Kripya aisi bhasha ka use na karein, warna aapko block kiya ja sakta hai!"
        )
        return

    # 2. Normal messages ke liye auto-reply ya menu
    else:
        bot.reply_to(message, "🤖 Maaf kijiye, main samajh nahi paya. Menu ya options dekhne ke liye /start dabayein.")
