    try:
        btn_approve = InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{qr_pkg_key}")
        btn_reject = InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}_{qr_pkg_key}")
        admin_keyboard = InlineKeyboardMarkup([[btn_approve, btn_reject]])
        admin_caption = (
            "📥 **Payment Screenshot Verification**\n\n"
            f"👤 **User:** {user.full_name} (`{user.id}`)\n"
            f"📦 **Package:** {pkg['name']}\n"
            f"💸 **Offer Price:** **{price_str}**"
        )
        await context.bot.send_photo(
            chat_id=ADMIN_USER_ID,
            photo=photo_obj.file_id,
            caption=admin_caption,
            reply_markup=admin_keyboard,
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Admin send error: {e}")
        
