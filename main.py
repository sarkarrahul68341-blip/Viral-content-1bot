markup = types.InlineKeyboardMarkup()

# Har button ko alag row mein add karne ke liye unhe alag-alag add karein:
btn1 = types.InlineKeyboardButton("🎛️ Buttons Editor", callback_data="buttons_editor")
btn2 = types.InlineKeyboardButton("📝 Posts Editor", callback_data="posts_editor")
btn3 = types.InlineKeyboardButton("💵 Balance", callback_data="balance_menu")

# Ek ke upar ek rakhne ke liye sabko alag add() karein:
markup.add(btn1)
markup.add(btn2)
markup.add(btn3)
