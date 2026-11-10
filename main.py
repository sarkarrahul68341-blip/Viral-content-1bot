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

# Official Support and Community Preview Links
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
# 3. START COMMAND & MAIN MENU HANDLER (8 PACKAGES)
# =====================================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command sent by users.
    Greets the user and presents the full menu with all 8 packages.
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
        
        # All 8 packages inline keyboard buttons
        keyboard = [
            [InlineKeyboardButton("⭐ 01 All mix content VIP Access", callback_data="pack_1")],
            [InlineKeyboardButton("🔑 02 Rap & Big File VD", callback_data="pack_2")],
            [InlineKeyboardButton("🔥 03 Special Update Pack", callback_data="pack_3")],
            [InlineKeyboardButton("💎 04 Mega Archive VIP", callback_data="pack_4")],
            [InlineKeyboardButton("🚀 05 Fast Server Access", callback_data="pack_5")],
            [InlineKeyboardButton("🎯 06 Exclusive Vault", callback_data="pack_6")],
            [InlineKeyboardButton("👑 07 Ultimate Lifetime Pass", callback_data="pack_7")],
            [InlineKeyboardButton("⚡ 08 Premium Direct Link", callback_data="pack_8")],
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
# 4. CALLBACK QUERY HANDLER (PACKAGES WITH PRICES, QR & LINKS)
# =====================================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all button clicks from the inline keyboards for all 8 packages,
    displaying their specific price, QR code info, and secure private link.
    """
    try:
        query = update.callback_query
        await query.answer()
        
        data = query.data
        logger.info(f"Callback query received: '{data}' from user ID: {query.from_user.id}")
        
        # Database/Structure for all 8 packages (Title, Price, QR/Payment Info, Private Link)
        packages_data = {
            "pack_1": {
                "title": "⭐ **01 All mix content VIP Access**",
                "price": "₹199 / Lifetime",
                "qr_info": "Scan below or pay via UPI to our official scanner/ID.",
                "private_link": "https://t.me/+T_Rwn6XiNPsyMDg9"  # Apne channel ka link yahan daal sakti hain
            },
            "pack_2": {
                "title": "🔑 **02 Rap & Big File VD**",
                "price": "₹249 / Lifetime",
                "qr_info": "Scan below or pay via UPI to our official scanner/ID.",
                "private_link": "https://t.me/+T_Rwn6XiNPsyMDg9"
            },
            "pack_3": {
                "title": "🔥 **03 Special Update Pack**",
                "price": "₹299 / Lifetime",
                "qr_info": "Scan below or pay via UPI to our official scanner/ID.",
                "private_link": "https://t.me/+T_Rwn6XiNPsyMDg9"
            },
            "pack_4": {
                "title": "💎 **04 Mega Archive VIP**",
                "price": "₹349 / Lifetime",
                "qr_info": "Scan below or pay via UPI to our official scanner/ID.",
                "private_link": "https://t.me/+T_Rwn6XiNPsyMDg9"
            },
            "pack_5": {
                "title": "🚀 **05 Fast Server Access**",
                "price": "₹149 / Lifetime",
                "qr_info": "Scan below or pay via UPI to our official scanner/ID.",
                "private_link": "https://t.me/+T_Rwn6XiNPsyMDg9"
            },
            "pack_6": {
                "title": "🎯 **06 Exclusive Vault**",
                "price": "₹399 / Lifetime",
                "qr_info": "Scan below or pay via UPI to our official scanner/ID.",
                "private_link": "https://t.me/+T_Rwn6XiNPsyMDg9"
            },
            "pack_7": {
                "title": "👑 **07 Ultimate Lifetime Pass**",
                "price": "₹499 / Lifetime",
                "qr_info": "Scan below or pay via UPI to our official scanner/ID.",
                "private_link": "https://t.me/+T_Rwn6XiNPsyMDg9"
            },
            "pack_8": {
                "title": "⚡ **08 Premium Direct Link**",
                "price": "₹199 / Lifetime",
                "qr_info": "Scan below or pay via UPI to our official scanner/ID.",
                "private_link": "https://t.me/+T_Rwn6XiNPsyMDg9"
            }
        }
        
        if data in packages_data:
            pkg = packages_data[data]
            package_text = (
                f"{pkg['title']}\n\n"
                f"💰 **Price:** {pkg['price']}\n\n"
                f"✨ **Package Highlights:**\n"
                f"• Full secure access to private channel.\n"
                f"• Daily regular updates & fresh uploads.\n"
                f"• High-speed secure download links.\n\n"
                f"💳 **Payment & QR Instructions:**\n"
                f"• {pkg['qr_info']}\n"
                f"• Send your payment screenshot here in the chat for instant verification.\n\n"
                f"🔗 **Access Link:** [Click Here to Join Channel after Payment]({pkg['private_link']})\n\n"
                f"👉 Need help? Contact support below:"
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
                [InlineKeyboardButton("🔥 03 Special Update Pack", callback_data="pack_3")],
                [InlineKeyboardButton("💎 04 Mega Archive VIP", callback_data="pack_4")],
                [InlineKeyboardButton("🚀 05 Fast Server Access", callback_data="pack_5")],
                [InlineKeyboardButton("🎯 06 Exclusive Vault", callback_data="pack_6")],
                [InlineKeyboardButton("👑 07 Ultimate Lifetime Pass", callback_data="pack_7")],
                [InlineKeyboardButton("⚡ 08 Premium Direct Link", callback_data="pack_8")],
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
    logger.info("Initializing Viral VIP Access Telegram bot application with 8 packages & prices...")
    
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
        
