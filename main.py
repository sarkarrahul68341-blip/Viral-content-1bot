import os
import re
import json
import time
import asyncio
import threading
import urllib.parse
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9210267090:AAFGulP572uIzyKPEGVa01y7HuR9xt2adio").strip()
UPI_ID = os.getenv("UPI_ID", "Puja6489@ptyes")
BIZ_NAME = os.getenv("BUSINESS_NAME", "All Max Content Bot")
ADMIN_ID = int(os.getenv("ADMIN_USER_ID", "8776203848"))
SUPPORT_URL = "https://t.me/+T_Rwn6XiNPsyMDg9"
DEMO_URL = "https://t.me/+w4MJrYfZ2zIyMTQ1"
DEFAULT_PHOTO = os.getenv("DEFAULT_PHOTO", "").strip()
PKG_PHOTO = "VIP New.jpg"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMOS_FILE = os.path.join(BASE_DIR, "demos_store.json")
CONFIG_FILE = os.path.join(BASE_DIR, "bot_config.json")
DEMO_FRAME_WIDTH = 1280
DEMO_FRAME_HEIGHT = 720
USED_SS = {}


def load_json_file(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Load err ({path}): {e}")
    return {}


def save_json_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Save err ({path}): {e}")


def load_demos():
    raw = load_json_file(DEMOS_FILE)
    return {int(k): v for k, v in raw.items()} if isinstance(raw, dict) else {}


def save_demos(demos_dict):
    save_json_file(DEMOS_FILE, demos_dict)


saved_cfg = load_json_file(CONFIG_FILE)

STORAGE = {
    "welcome": saved_cfg.get("welcome") or DEFAULT_PHOTO,
    "banner": saved_cfg.get("banner") or os.getenv("BANNER_PHOTO", PKG_PHOTO).strip(),
    "demos": load_demos(),
}


def save_config():
    save_json_file(CONFIG_FILE, {
        "welcome": STORAGE.get("welcome", ""),
        "banner": STORAGE.get("banner", ""),
    })


PACKAGES = {
    "file_1": {"name": "01 All mix content VIP Access", "price": 249, "badge": "4̶9̶9̶ ➡️ 💎 ₹249", "emoji": "👑", "link": "https://t.me/+s4Zzmwni59diNjU1"},
    "file_2": {"name": "02 Rap & Big File VD", "price": 89, "badge": "1̶9̶9̶ ➡️ ⚡ ₹89", "emoji": "🎬", "link": "https://t.me/+_AILkUGhVnVkMzBl"},
    "file_3": {"name": "03 Mom and Son Real Sex", "price": 45, "badge": "9̶9̶ ➡️ 🔥 ₹45", "emoji": "💋", "link": "https://t.me/+qjTxEmHC-z4wMzE1"},
    "file_4": {"name": "04 Insta viral reels and sex", "price": 40, "badge": "9̶9̶ ➡️ ✨ ₹40", "emoji": "📱", "link": "https://t.me/+LmzeU14SK_I0MGY9"},
    "file_5": {"name": "05 Ganga bath group join", "price": 199, "badge": "3̶9̶9̶ ➡️ 👑 ₹199", "emoji": "🌊", "link": "https://t.me/+jMs1EZ3RLSc1Yjhl"},
    "file_6": {"name": "06 Bath camera hidden", "price": 55, "badge": "1̶2̶9̶ ➡️ 💥 ₹55", "emoji": "🎥", "link": "https://t.me/+G4yBWASYMzYzOTc9"},
    "file_7": {"name": "07 CP girl real fuke", "price": 65, "badge": "1̶4̶9̶ ➡️ 🌟 ₹65", "emoji": "✨", "link": "https://t.me/+f9i3BlsoUeZiZmY1"},
    "file_8": {"name": "08 Sister and brother sex", "price": 30, "badge": "7̶9̶ ➡️ 💖 ₹30", "emoji": "❤️", "link": "https://t.me/+BYOIdmg4w3c2MjQ1"},
}

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()
loop = asyncio.new_event_loop()
threading.Thread(target=lambda: (asyncio.set_event_loop(loop), loop.run_forever()), daemon=True).start()


async def _boot():
    await bot_app.initialize()
    await bot_app.start()


asyncio.run_coroutine_threadsafe(_boot(), loop).result(timeout=30)


def _sync_webhook():
    url = (os.getenv("RENDER_EXTERNAL_URL") or "https://viral-content-1bot-1.onrender.com").rstrip("/")
    try:
        asyncio.run_coroutine_threadsafe(bot_app.bot.set_webhook(f"{url}/{TOKEN}"), loop).result(timeout=10)
    except Exception as e:
        print(f"Webhook err: {e}")


threading.Thread(target=_sync_webhook, daemon=True).start()


async def send_safe(context, chat_id, photo, caption, markup, video=None, video_meta=None):
    if video:
        meta = video_meta or {}
        try:
            return await context.bot.send_video(
                chat_id,
                video,
                caption=caption,
                reply_markup=markup,
                parse_mode="Markdown",
                width=DEMO_FRAME_WIDTH,
                height=DEMO_FRAME_HEIGHT,
                duration=meta.get("duration"),
                supports_streaming=True,
            )
        except BadRequest:
            pass
    if photo:
        try:
            if os.path.exists(photo):
                with open(photo, "rb") as f:
                    return await context.bot.send_photo(chat_id, f, caption=caption, reply_markup=markup, parse_mode="Markdown")
            return await context.bot.send_photo(chat_id, photo, caption=caption, reply_markup=markup, parse_mode="Markdown")
        except BadRequest:
            pass
    return await context.bot.send_message(chat_id, caption, reply_markup=markup, parse_mode="Markdown")


def make_qr(amount, uid):
    uri = f"upi://pay?pa={UPI_ID}&pn={urllib.parse.quote(BIZ_NAME)}&am={amount}&cu=INR&tn=Order_{uid}"
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path = f"qr_{uid}.png"
    img.save(path, optimize=True)
    return path


def menu_kb():
    rows = [[InlineKeyboardButton(f"{p['emoji']} {p['name']} • {p['badge']} 👉", callback_data=k)] for k, p in PACKAGES.items()]
    rows.append([InlineKeyboardButton("🎁 🅵🆁🅴🅴   __   🅳🅴🅼🅾", callback_data="demo_1")])
    rows.append([InlineKeyboardButton("💬 Help & Support", url=SUPPORT_URL)])
    return InlineKeyboardMarkup(rows)


async def start(update: Update, context):
    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.delete()
        except Exception:
            pass
    photo = STORAGE.get("welcome") or STORAGE.get("banner") or (PKG_PHOTO if os.path.exists(PKG_PHOTO) else "")
    caption = (
        "❤️ **Welcome to All Max Content Bot!**\n\n"
        "🔥 **Special Discount Offer Chal Raha Hai!**\n"
        "✅ Direct UPI QR Payment • Fast Approval • Instant Access\n\n"
        "👇 Niche se apna package select karein:"
    )
    await send_safe(context, update.effective_chat.id, photo, caption, menu_kb())


async def setwelcome_cmd(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["pending_welcome"] = True
    await update.message.reply_text(
        "🖼️ **Welcome Banner Ready!**\n"
        "📸 Ab apna naya **welcome banner photo** bhej dein.",
        parse_mode="Markdown"
    )


async def setdemo_cmd(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    args = context.args or []
    if not args or not re.fullmatch(r"\d{1,2}", args[0]):
        await update.message.reply_text("⚠️ Sahi format use karein: `/setdemo 1` (1 se 10 tak)", parse_mode="Markdown")
        return
    idx = max(1, min(10, int(args[0])))
    note = " ".join(args[1:]).strip()
    context.user_data["pending_demo"] = {"idx": idx, "note": note}
    await update.message.reply_text(
        f"🎬 **Demo {idx} Ready!**\n"
        f"🎥 Ab iske liye **video** ya **photo** bhej dein.",
        parse_mode="Markdown"
    )


async def deldemo_cmd(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    args = context.args or []
    if not args:
        await update.message.reply_text("⚠️ Sahi format use karein: `/deldemo 1` (ya `/deldemo all`)", parse_mode="Markdown")
        return
    demos = STORAGE.setdefault("demos", {})
    if args[0].lower() == "all":
        demos.clear()
        save_demos(demos)
        await update.message.reply_text("🗑️ **Saare demos delete ho gaye!** Ab aap `/setdemo 1` se naye set kar sakte hain.", parse_mode="Markdown")
        return
    if not re.fullmatch(r"\d{1,2}", args[0]):
        await update.message.reply_text("⚠️ Sahi format use karein: `/deldemo 1` (1 se 10 tak) ya `/deldemo all`", parse_mode="Markdown")
        return
    idx = max(1, min(10, int(args[0])))
    if idx in demos:
        del demos[idx]
        save_demos(demos)
        await update.message.reply_text(f"🗑️ **Demo {idx} delete ho gaya!** Ab aap `/setdemo {idx}` se naya set kar sakte hain.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"ℹ️ Demo {idx} pehle se khali hai.", parse_mode="Markdown")


async def demos_status(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    demos = STORAGE.get("demos", {})
    if not demos:
        await update.message.reply_text("ℹ️ Abhi koi demo set nahi hai. `/setdemo 1` bhej kar video ya photo bhejein.", parse_mode="Markdown")
        return
    lines = ["🎬 **Saved Permanent Demos (1-10):**"]
    for i in sorted(demos.keys()):
        kind = "Video" if demos[i].get("video") else "Photo"
        lines.append(f"• #{i} ({kind}): {demos[i].get('note', '')}")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def on_video(update: Update, context):
    msg = update.message
    if not msg or not msg.video or update.effective_user.id != ADMIN_ID:
        return

    caption_text = (msg.caption or "").strip()
    pending = context.user_data.pop("pending_demo", None)
    match = re.match(r"^/setdemo\s+(\d{1,2})(?:\s+(.*))?$", caption_text, flags=re.IGNORECASE | re.DOTALL)

    if match or pending:
        if match:
            idx = max(1, min(10, int(match.group(1))))
            custom_note = (match.group(2) or "").strip()
        else:
            idx = int(pending["idx"])
            custom_note = caption_text or (pending.get("note") or "")
        demos = STORAGE.setdefault("demos", {})
        demos[idx] = {
            "video": msg.video.file_id,
            "width": DEMO_FRAME_WIDTH,
            "height": DEMO_FRAME_HEIGHT,
            "duration": msg.video.duration,
            "note": custom_note,
        }
        save_demos(demos)
        await msg.reply_text(f"✅ **Demo {idx} (Video) permanently save ho gaya!** 🎬", parse_mode="Markdown")


async def on_photo(update: Update, context):
    msg = update.message
    if not msg or not msg.photo:
        return

    caption_text = (msg.caption or "").strip()
    lower_cap = caption_text.lower()

    if update.effective_user.id == ADMIN_ID:
        pending_welcome = context.user_data.pop("pending_welcome", False)
        if pending_welcome or "setwelcome" in lower_cap or "setbanner" in lower_cap:
            fid = msg.photo[-1].file_id
            STORAGE["welcome"] = fid
            STORAGE["banner"] = fid
            save_config()
            await msg.reply_text("✅ **Welcome banner permanently save ho gaya!** 🖼️", parse_mode="Markdown")
            return

        pending = context.user_data.pop("pending_demo", None)
        match = re.match(r"^/setdemo\s+(\d{1,2})(?:\s+(.*))?$", caption_text, flags=re.IGNORECASE | re.DOTALL)
        if match or pending:
            if match:
                idx = max(1, min(10, int(match.group(1))))
                custom_note = (match.group(2) or "").strip()
            else:
                idx = int(pending["idx"])
                custom_note = caption_text or (pending.get("note") or "")
            demos = STORAGE.setdefault("demos", {})
            demos[idx] = {
                "photo": msg.photo[-1].file_id,
                "note": custom_note,
            }
            save_demos(demos)
            await msg.reply_text(f"✅ **Demo {idx} (Photo) permanently save ho gaya!** 💾", parse_mode="Markdown")
            return

    pkg_key = context.user_data.get("qr_pkg")
    uid_obj = msg.photo[-1].file_unique_id
    now = time.time()
    for k in [k for k, ts in USED_SS.items() if now - ts >= 86400]:
        del USED_SS[k]

    if not pkg_key or pkg_key not in PACKAGES or uid_obj in USED_SS or getattr(msg, "forward_date", None):
        await msg.reply_text("⚠️ Kripya pehle package select karke **Pay Now** se payment karein, uske baad payment ka original screenshot bhejein. 📸", parse_mode="Markdown")
        return

    USED_SS[uid_obj] = now
    context.user_data.pop("qr_pkg", None)
    pkg = PACKAGES[pkg_key]
    user = update.effective_user

    await msg.reply_text(
        f"⏳ **Payment Screenshot Received!**\n"
        f"📦 **Package:** {pkg['name']}\n"
        f"💰 **Amount:** {pkg['badge']}\n\n"
        f"✅ Aapka payment verification ke liye bhej diya gaya hai. Approve hote hi aapko **VIP Access Link** yahin mil jaayega. 🚀",
        parse_mode="Markdown"
    )
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{pkg_key}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}_{pkg_key}"),
    ]])
    await context.bot.send_photo(
        ADMIN_ID, msg.photo[-1].file_id,
        caption=f"📥 **Payment Proof**\n👤 {user.full_name} (`{user.id}`)\n📦 {pkg['name']} • **{pkg['badge']}**",
        reply_markup=kb, parse_mode="Markdown"
    )


async def on_callback(update: Update, context):
    q = update.callback_query
    await q.answer()
    data, uid, cid = q.data, q.from_user.id, q.message.chat_id

    if data == "main_menu":
        await start(update, context)
        return

    if data == "ss_guide":
        try:
            await q.message.delete()
        except Exception:
            pass
        await context.bot.send_message(
            cid,
            "📸 **Screenshot Yahin Bhejein!**\n\n"
            "✅ Payment karne ke baad **seedha is bot chat mein** (neeche 📎 / photo icon se) apna screenshot bhej dein.\n"
            "⏳ Bhejte hi aapka proof verification ke liye chala jaayega.\n"
            "🚀 Approve hote hi **VIP Access Link** yahin mil jaayega.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")],
            ]),
            parse_mode="Markdown"
        )
        return

    if data.startswith(("approve_", "reject_")) and uid == ADMIN_ID:
        act, target_id, key = data.split("_", 2)
        pkg = PACKAGES.get(key, PACKAGES["file_1"])
        if act == "approve":
            await context.bot.send_message(
                int(target_id),
                f"✅ **Payment Approved!** 🎉\n"
                f"📦 **Package:** {pkg['name']}\n"
                f"💰 **Paid:** {pkg['badge']}\n\n"
                f"🚀 Niche button par click karke apna VIP access open karein:",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔓 Access VIP Link 🚀", url=pkg["link"])]]),
                parse_mode="Markdown"
            )
        else:
            await context.bot.send_message(
                int(target_id),
                f"❌ **Payment Not Verified**\n"
                f"📦 **Package:** {pkg['name']}\n\n"
                f"📸 Kripya sahi payment screenshot bhejein ya **Help & Support** se sampark karein. 💬",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Help & Support", url=SUPPORT_URL)]]),
                parse_mode="Markdown"
            )
        return

    if data.startswith("demo_"):
        idx = max(1, min(10, int(data.replace("demo_", "") or 1)))
        row = []
        if idx > 1:
            row.append(InlineKeyboardButton("⬅️ Prev Clip", callback_data=f"demo_{idx - 1}"))
        if idx < 10:
            row.append(InlineKeyboardButton("Next Clip ➡️", callback_data=f"demo_{idx + 1}"))
        rows = [row] if row else []
        if idx == 10:
            rows.append([InlineKeyboardButton("👑 Get Full VIP Access • 4̶9̶9̶ ➡️ 💎 ₹249", callback_data="file_1")])
        rows.append([InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")])
        rows.append([InlineKeyboardButton("🎬 Join Demo 2", url=DEMO_URL)])
        try:
            await q.message.delete()
        except Exception:
            pass
        demo_item = STORAGE.get("demos", {}).get(idx, {})
        video = demo_item.get("video")
        video_meta = {
            "width": DEMO_FRAME_WIDTH,
            "height": DEMO_FRAME_HEIGHT,
            "duration": demo_item.get("duration"),
        }
        photo = demo_item.get("photo") or STORAGE.get("welcome") or STORAGE.get("banner") or (PKG_PHOTO if os.path.exists(PKG_PHOTO) else "")
        custom_line = (demo_item.get("note") or "").strip()
        demo_caption = (
            f"✨ **Preview ({idx}/10)** ✨\n\n"
            f"👑 **Poore Full Access Plan par aapko sab kuch ek saath mil jaayega!** 💎"
            + (f"\n🔥 {custom_line} 🚀" if custom_line else "")
        )
        await send_safe(context, cid, photo, demo_caption, InlineKeyboardMarkup(rows), video=video, video_meta=video_meta)
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        banner = STORAGE.get("banner") or STORAGE.get("welcome") or (PKG_PHOTO if os.path.exists(PKG_PHOTO) else "")
        text = (
            f"💎 **Selected Plan:** {pkg['name']} {pkg['emoji']}\n"
            f"💰 **Offer Price:** {pkg['badge']}\n\n"
            f"🛡️ **How it works:**\n"
            f"1️⃣ ⚡ Niche **Pay Now** dabakar QR code generate karein.\n"
            f"2️⃣ 📱 UPI se **₹{pkg['price']}** pay karke payment **screenshot** bhejein.\n"
            f"3️⃣ 🚀 Verification ke baad aapko turant **VIP Access Link** mil jaayega.\n\n"
            f"🔒 *100% direct UPI payment • Safe & fast verification.*"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"⚡ Pay Now • {pkg['badge']}", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")],
        ])
        try:
            await q.message.delete()
        except Exception:
            pass
        await send_safe(context, cid, banner, text, kb)
        return

    if data.startswith("pay_"):
        key = data.replace("pay_", "")
        pkg = PACKAGES.get(key)
        if not pkg:
            return
        context.user_data["qr_pkg"] = key
        qr_path = make_qr(pkg["price"], uid)
        try:
            try:
                await q.message.delete()
            except Exception:
                pass
            cap = (
                f"📱 **SCAN & PAY**\n"
                f"💎 **Package:** {pkg['name']} {pkg['emoji']}\n"
                f"💰 **Amount:** {pkg['badge']}\n\n"
                f"1️⃣ 📷 Upar diye gaye QR code ko scan karke **₹{pkg['price']}** pay karein (`{UPI_ID}`).\n"
                f"2️⃣ 📸 Payment ke baad **yahin is chat mein** screenshot bhejein.\n"
                f"3️⃣ 🚀 Verification ke baad aapko turant **VIP Link** yahin mil jaayega.\n\n"
                f"🛡️ *100% direct UPI payment • Safe & fast verification.*"
            )
            with open(qr_path, "rb") as f:
                await context.bot.send_photo(
                    cid, f, caption=cap,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📸 Send Screenshot Here", callback_data="ss_guide")],
                        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")],
                    ]),
                    parse_mode="Markdown"
                )
        finally:
            if os.path.exists(qr_path):
                os.remove(qr_path)


bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("setwelcome", setwelcome_cmd))
bot_app.add_handler(CommandHandler("setdemo", setdemo_cmd))
bot_app.add_handler(CommandHandler("deldemo", deldemo_cmd))
bot_app.add_handler(CommandHandler("demos", demos_status))
bot_app
