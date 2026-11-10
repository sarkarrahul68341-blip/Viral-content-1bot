import os
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# =====================================================================
# 1. LOGGING & SYSTEM CONFIGURATION SETUP
# =====================================================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token (Updated securely to Viral VIP Access token)
TOKEN = os.getenv("TELEGRAM_TOKEN", "9251056494:AAG-i-lewl5C1yrJgXLncwFlmm60UddSNa8")

# Official Support and Community Preview Links from Active Context
SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"
DEMO_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"


# =====================================================================
# 2. FLASK APP CONFIGURATION FOR RENDER 24/7 KEEP-ALIVE
# =====================================================================
app = Flask(__name__)

@app.route('/')
def home():
    """Health check route for Render web service to prevent sleeping"""
    return "Viral VIP Access Bot is running live, secure, and fully operational 24/7!"


# =====================================================================
# 3. START COMMAND & MAIN MENU HANDLER
# =====================================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command sent by users.
    Greets the user and presents the main interactive package menu.
    """
    try:
        user = update.effective_user
        user_name = user.first_name if user else "Valued User"
        
        logger.info(f"Incoming /start command from user: {user_name} (ID: {user.id if user else 'Unknown'})")
        
        welcome_text = (
            f"Hello **{user_name}**!\n\n"
            f"Welcome to **Viral VIP Access** 🚀\n\n"
            f"Get instant access to exclusive premium content, high-speed big files, "
            f"and regular daily updates.\n\n"
            f"📌 **Please choose from the available packages below:**"
        )
        
        # Interactive inline keyboard buttons matching your exact requirements
        keyboard = [
            [InlineKeyboardButton("⭐ 01 All mix content VIP Access", callback_data="pack_1")],
            [InlineKeyboardButton("🔑 02 Rap & Big File VD", callback_data="pack_2")],
            [InlineKeyboardButton("🎬 Free Demo & Preview", url=DEMO_LINK)],
            [InlineKeyboardButton("📞 Support & Help", url=SUPPORT_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(
                text=welcome_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Error occurred in start handler: {e}")


# =====================================================================
# 4. CALLBACK QUERY HANDLER (PACKAGES, DETAILS & NAVIGATION)
# =====================================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all button clicks from the inline keyboards (Package details & menu navigation).
    """
    try:
        query = update.callback_query
        await query.answer()
        
        data = query.data
        logger.info(f"Callback query received: '{data}' from user ID: {query.from_user.id}")
        
        if data == "pack_1":
            package_text = (
                "⭐ **01 All mix content VIP Access**\n\n"
                "✨ **Package Highlights:**\n"
                "• Full lifetime access to all mix content channels.\n"
                "• Daily regular updates & fresh uploads.\n"
                "• High-speed secure server links.\n\n"
                "💳 **Payment Instructions:**\n"
                "1. Complete your UPI payment to our official scanner/ID.\n"
                "2. Send your payment screenshot here in the chat.\n"
                "3. Your private access link will be shared instantly upon verification.\n\n"
                "👉 Click below to contact support after payment:"
            )
            keyboard = [
                [InlineKeyboardButton("💬 Send Payment Screenshot / Verify", url=SUPPORT_LINK)],
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_text(
                text=package_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )

        elif data == "pack_2":
            package_text = (
                "🔑 **02 Rap & Big File VD**\n\n"
                "✨ **Package Highlights:**\n"
                "• Access to exclusive high-resolution rap videos & big file archives.\n"
                "• Direct fast-download links with zero speed limits.\n"
                "• Premium private channel membership.\n\n"
                "💳 **Payment Instructions:**\n"
                "1. Complete your UPI transaction.\n"
                "2. Share the transaction screenshot with support.\n"
                "3. Get added to the private archive immediately.\n\n"
                "👉 Click below to contact support after payment:"
            )
            keyboard = [
                [InlineKeyboardButton("💬 Send Payment Screenshot / Verify", url=SUPPORT_LINK)],
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_text(
                text=package_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )

        elif data == "main_menu":
            user_name = query.from_user.first_name if query.from_user else "Valued User"
            welcome_text = (
                f"Hello **{user_name}**!\n\n"
                f"Welcome back to **Viral VIP Access** 🚀\n"
                f"Please choose from the available packages below:"
            )
            keyboard = [
                [InlineKeyboardButton("⭐ 01 All mix content VIP Access", callback_data="pack_1")],
                [InlineKeyboardButton("🔑 02 Rap & Big File VD", callback_data="pack_2")],
                [InlineKeyboardButton("🎬 Free Demo & Preview", url=DEMO_LINK)],
                [InlineKeyboardButton("📞 Support & Help", url=SUPPORT_LINK)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_text(
                text=welcome_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Error occurred in button handler: {e}")


# =====================================================================
# 5. PAYMENT SCREENSHOT & USER MESSAGE HANDLER
# =====================================================================
async def handle_user_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles incoming text messages, images, or payment screenshots sent by users
    and guides them to the support chat for swift verification.
    """
    try:
        if update.message:
            user_id = update.message.from_user.id
            logger.info(f"Received message/photo from user ID: {user_id}")
            
            if update.message.photo:
                reply_response = (
                    "📸 **Payment Screenshot Successfully Received!**\n\n"
                    "Thank you for sharing. Our team is verifying your transaction details. "
                    "If verification takes a moment, please click below to ping support directly:"
                )
            else:
                reply_response = (
                    "✅ Message received successfully!\n\n"
                    "If you are looking to purchase a VIP package or need instant assistance, "
                    "please connect with our support team:"
                )
            
            keyboard = [[InlineKeyboardButton("📞 Open Support Chat", url=SUPPORT_LINK)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                text=reply_response,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Error handling user message: {e}")


# =====================================================================
# 6. MAIN APPLICATION INITIALIZATION & EXECUTION LOOP
# =====================================================================
def main():
    """Main entry point to build the application and start polling and Flask web server."""
    logger.info("Initializing Viral VIP Access Telegram bot application...")
    
    # Build Telegram Bot application using the updated token
    application = Application.builder().token(TOKEN).build()

    # Registering all necessary handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO & ~filters.COMMAND, handle_user_messages))

    # Determine port for Render deployment
    port_num = int(os.environ.get("PORT", 8080))
    
    # Launch Flask keep-alive server in a separate background daemon thread
    logger.info(f"Starting Flask keep-alive web server on port {port_num}...")
    flask_thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=port_num, debug=False, use_reloader=False)
    )
    flask_thread.daemon = True
    flask_thread.start()

    # Start the bot polling loop
    logger.info("Starting Telegram bot polling loop... Bot is now live!")
    application.run_polling()


if __name__ == "__main__":
    main()
        
