import os, re, json, time, asyncio, threading, urllib.parse, qrcode
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
PKG_PHOTO = "VIP New.jpg"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMOS_FILE, CONFIG_FILE = os.path.join(BASE_DIR, "demos_store.json"), os.path.join(BASE_DIR, "bot_config.json")
W, H = 1280, 720
USED_SS = {}


def r_json(p):
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def w_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


cfg = r_json(CONFIG_FILE)
STORAGE = {
    "welcome": cfg.get("welcome") or os.getenv("DEFAULT_PHOTO", "").strip(),
    "banner": cfg.get("banner") or os.getenv("BANNER_PHOTO", PKG_PHOTO).strip(),
    "demos": {int(k): v for k, v in r_json(DEMOS_FILE).items()},
}

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


async def send_safe(context, chat_id, photo, caption, markup, video=None, dur=None):
    if video:
        try:
            return await context.bot.send_video(chat_id, video, caption=caption, reply_markup=markup, parse_mode="Markdown", width=W, height=H, duration=dur, supports_streaming=True)
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
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
    qr.add_data(uri)
    qr.make(fit=True)
    path = f"qr_{uid}.png"
    qr.make_image(fill_color="black", back_color="white").save(path, optimize=True)
    return path


def menu_kb():
    rows = [[InlineKeyboardButton(f"{p['emoji']} {p['name']} • {p['badge']} 👉", callback_data=k)] for k, p in PACKAGES.items()]
    rows.append([InlineKeyboardButton("🎁 🅵🆁🅴🅴   __   🅳🅴🅼🅾", callback_data="demo_1")])
    rows.append([InlineKeyboardButton("💬 Help & Support", url=SUPPORT_URL)])
    return InlineKeyboardMarkup(rows)


async def del_msg(q):
    try:
        await q.message.delete()
    except Exception:
        pass


async def start(update: Update, context):
    if update.callback_query:
        await update.callback_query.answer()
        await del_msg(update.callback_query)
    photo = STORAGE.get("welcome") or STORAGE.get("banner") or (PKG_PHOTO if os.path.exists(PKG_PHOTO) else "")
    cap = "❤️ **Welcome to All Max Content Bot!**\n\n🔥 **Special Discount Offer Chal Raha Hai!**\n✅ Direct UPI QR Payment • Fast Approval • Instant Access\n\n👇 Niche se apna package select karein:"
    await send_safe(context, update.effective_chat.id, photo, cap, menu_kb())


async def setwelcome_cmd(update: Update, context):
    if update.effective_user.id == ADMIN_ID:
        context.user_data["pending_welcome"] = True
        await update.message.reply_text("🖼️ **Welcome Banner Ready!** 📸 Ab photo bhej dein.", parse_mode="Markdown")


async def setdemo_cmd(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    args = context.args or []
    if not args or not re.fullmatch(r"\d{1,2}", args[0]):
        await update.message.reply_text("⚠️ Use: `/setdemo 1` (1-10)", parse_mode="Markdown")
        return
    idx = max(1, min(10, int(args[0])))
    context.user_data["pending_demo"] = {"idx": idx, "note": " ".join(args[1:]).strip()}
    await update.message.reply_text(f"🎬 **Demo {idx} Ready!** 🎥 Ab video ya photo bhej dein.", parse_mode="Markdown")


async def deldemo_cmd(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    args = context.args or []
    demos = STORAGE.setdefault("demos", {})
    if args and args[0].lower() == "all":
        demos.clear()
        w_json(DEMOS_FILE, demos)
        await update.message.reply_text("🗑️ **Saare demos delete ho gaye!**", parse_mode="Markdown")
        return
    if not args or not re.fullmatch(r"\d{1,2}", args[0]):
        await update.message.reply_text("⚠️ Use: `/deldemo 1` ya `/deldemo all`", parse_mode="Markdown")
        return
    idx = max(1, min(10, int(args[0])))
    if demos.pop(idx, None) is not None:
        w_json(DEMOS_FILE, demos)
        await update.message.reply_text(f"🗑️ **Demo {idx} delete ho gaya!**", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"ℹ️ Demo {idx} khali hai.", parse_mode="Markdown")


async def demos_status(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    demos = STORAGE.get("demos", {})
    if not demos:
        await update.message.reply_text("ℹ️ Koi demo set nahi hai. `/setdemo 1` bhejein.", parse_mode="Markdown")
        return
    lines = ["🎬 **Saved Demos (1-10):**"] + [f"• #{i} ({'Video' if demos[i].get('video') else 'Photo'}): {demos[i].get('note', '')}" for i in sorted(demos)]
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


def save_demo_entry(context, caption_text, payload):
    pending = context.user_data.pop("pending_demo", None)
    m = re.match(r"^/setdemo\s+(\d{1,2})(?:\s+(.*))?$", caption_text, flags=re.IGNORECASE | re.DOTALL)
    if not (m or pending):
        return None
    idx = max(1, min(10, int(m.group(1)))) if m else int(pending["idx"])
    note = (m.group(2) or "").strip() if m else (caption_text or pending.get("note") or "")
    entry = dict(payload, note=note)
    STORAGE.setdefault("demos", {})[idx] = entry
    w_json(DEMOS_FILE, STORAGE["demos"])
    return idx


async def on_video(update: Update, context):
    msg = update.message
    if msg and msg.video and update.effective_user.id == ADMIN_ID:
        idx = save_demo_entry(context, (msg.caption or "").strip(), {"video": msg.video.file_id, "duration": msg.video.duration})
        if idx:
            await msg.reply_text(f"✅ **Demo {idx} (Video) save ho gaya!** 🎬", parse_mode="Markdown")


async def on_photo(update: Update, context):
    msg = update.message
    if not msg or not msg.photo:
        return
    cap = (msg.caption or "").strip()
    if update.effective_user.id == ADMIN_ID:
        if context.user_data.pop("pending_welcome", False) or any(w in cap.lower() for w in ("setwelcome", "setbanner")):
            fid = msg.photo[-1].file_id
            STORAGE["welcome"] = STORAGE["banner"] = fid
            w_json(CONFIG_FILE, {"welcome": fid, "banner": fid})
            await msg.reply_text("✅ **Welcome banner save ho gaya!** 🖼️", parse_mode="Markdown")
            return
        idx = save_demo_entry(context, cap, {"photo": msg.photo[-1].file_id})
        if idx:
            await msg.reply_text(f"✅ **Demo {idx} (Photo) save ho gaya!** 💾", parse_mode="Markdown")
            return

    pkg_key = context.user_data.get("qr_pkg")
    uid_obj = msg.photo[-1].file_unique_id
    now = time.time()
    for k in [k for k, ts in USED_SS.items() if now - ts >= 86400]:
        del USED_SS[k]
    if not pkg_key or pkg_key not in PACKAGES or uid_obj in USED_SS or getattr(msg, "forward_date", None):
        await msg.reply_text("⚠️ Kripya pehle package select karke **Pay Now** se payment karein, phir screenshot bhejein. 📸", parse_mode="Markdown")
        return

    USED_SS[uid_obj] = now
    context.user_data.pop("qr_pkg", None)
    pkg, user = PACKAGES[pkg_key], update.effective_user
    await msg.reply_text(f"⏳ **Screenshot Received!**\n📦 {pkg['name']}\n💰 {pkg['badge']}\n\n✅ Approve hote hi **VIP Link** yahin mil jaayega. 🚀", parse_mode="Markdown")
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{pkg_key}"), InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}_{pkg_key}")]])
    await context.bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=f"📥 **Proof**\n👤 {user.full_name} (`{user.id}`)\n📦 {pkg['name']} • **{pkg['badge']}**", reply_markup=kb, parse_mode="Markdown")


async def on_callback(update: Update, context):
    q = update.callback_query
    await q.answer()
    data, uid, cid = q.data, q.from_user.id, q.message.chat_id

    if data == "main_menu":
        await start(update, context)
    elif data == "ss_guide":
        await del_msg(q)
        await context.bot.send_message(cid, "📸 **Screenshot Yahin Bhejein!**\n\n✅ Seedha is chat mein photo bhej dein.\n🚀 Approve hote hi **VIP Access Link** yahin mil jaayega.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]]), parse_mode="Markdown")
    elif data.startswith(("approve_", "reject_")) and uid == ADMIN_ID:
        act, target_id, key = data.split("_", 2)
        pkg = PACKAGES.get(key, PACKAGES["file_1"])
        if act == "approve":
            await context.bot.send_message(int(target_id), f"✅ **Payment Approved!** 🎉\n📦 {pkg['name']}\n💰 {pkg['badge']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔓 Access VIP Link 🚀", url=pkg["link"])]]), parse_mode="Markdown")
        else:
            await context.bot.send_message(int(target_id), f"❌ **Payment Not Verified**\n📦 {pkg['name']}\n\n📸 Sahi screenshot bhejein ya support se sampark karein. 💬", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Help & Support", url=SUPPORT_URL)]]), parse_mode="Markdown")
    elif data.startswith("demo_"):
        idx = max(1, min(10, int(data.replace("demo_", "") or 1)))
        row = ([InlineKeyboardButton("⬅️ Prev Clip", callback_data=f"demo_{idx - 1}")] if idx > 1 else []) + ([InlineKeyboardButton("Next Clip ➡️", callback_data=f"demo_{idx + 1}")] if idx < 10 else [])
        rows = ([row] if row else []) + ([[InlineKeyboardButton("👑 Get Full VIP Access • 4̶9̶9̶ ➡️ 💎 ₹249", callback_data="file_1")]] if idx == 10 else []) + [[InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")], [InlineKeyboardButton("🎬 Join Demo 2", url=DEMO_URL)]]
        await del_msg(q)
        item = STORAGE.get("demos", {}).get(idx, {})
        line = (item.get("note") or "").strip()
        cap = f"✨ **Preview ({idx}/10)** ✨\n\n👑 **Poore Full Access Plan par aapko sab kuch ek saath mil jaayega!** 💎" + (f"\n🔥 {line} 🚀" if line else "")
        await send_safe(context, cid, item.get("photo") or STORAGE.get("welcome") or STORAGE.get("banner") or (PKG_PHOTO if os.path.exists(PKG_PHOTO) else ""), cap, InlineKeyboardMarkup(rows), video=item.get("video"), dur=item.get("duration"))
    elif data in PACKAGES:
        pkg = PACKAGES[data]
        banner = STORAGE.get("banner") or STORAGE.get("welcome") or (PKG_PHOTO if os.path.exists(PKG_PHOTO) else "")
        text = f"💎 **Selected Plan:** {pkg['name']} {pkg['emoji']}\n💰 **Offer Price:** {pkg['badge']}\n\n🛡️ **How it works:**\n1️⃣ ⚡ **Pay Now** dabakar QR code generate karein.\n2️⃣ 📱 UPI se **₹{pkg['price']}** pay karke **screenshot** bhejein.\n3️⃣ 🚀 Verification ke baad **VIP Access Link** yahin mil jaayega."
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(f"⚡ Pay Now • {pkg['badge']}", callback_data=f"pay_{data}")], [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]])
        await del_msg(q)
        await send_safe(context, cid, banner, text, kb)
    elif data.startswith("pay_"):
        pkg = PACKAGES.get(data.replace("pay_", ""))
        if not pkg:
            return
        context.user_data["qr_pkg"] = data.replace("pay_", "")
        qr_path = make_qr(pkg["price"], uid)
        try:
            await del_msg(q)
            cap = f"📱 **SCAN & PAY**\n💎 {pkg['name']} {pkg['emoji']}\n💰 {pkg['badge']}\n\n1️⃣ 📷 QR scan karke **₹{pkg['price']}** pay karein (`{UPI_ID}`).\n2️⃣ 📸 Payment ke baad **yahin** screenshot bhejein.\n3️⃣ 🚀 Approve hote hi **VIP Link** yahin mil jaayega."
            with open(qr_path, "rb") as f:
                await context.bot.send_photo(cid, f, caption=cap, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📸 Send Screenshot Here", callback_data="ss_guide")], [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]]), parse_mode="Markdown")
        finally:
            if os.path.exists(qr_path):
                os.remove(qr_path)


for cmd, fn in [("start", start), ("setwelcome", setwelcome_cmd), ("setdemo", setdemo_cmd), ("deldemo", deldemo_cmd), ("demos", demos_status)]:
    bot_app.add_handler(CommandHandler(cmd, fn))
bot_app.add_handler(CallbackQueryHandler(on_callback))
bot_app.add_handler(MessageHandler(filters.VIDEO, on_video))
bot_app.add_handler(MessageHandler(filters.PHOTO, on_photo))


@app.route("/")
def home():
    return "OK", 200


@app.route("/refresh")
def refresh_hook():
    _sync_webhook()
    return "Webhook Refreshed", 200


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        payload = request.get_json(force=True, silent=True)
        if payload:
            asyncio.run_coroutine_threadsafe(bot_app.process_update(Update.de_json(payload, bot_app.bot)), loop)
    except Exception as e:
        print(f"Update err: {e}")
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
