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
DEFAULT_WELCOME_PHOTO = os.getenv("DEFAULT_PHOTO", "").strip()
DEFAULT_WELCOME_GIF = os.getenv("DEFAULT_GIF", "").strip()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMOS_FILE = os.path.join(BASE_DIR, "demos_store.json")
CONFIG_FILE = os.path.join(BASE_DIR, "bot_config.json")
W, H, USED_SS = 1280, 720, {}


def r_json(p):
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def w_json(p, d):
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Write err: {e}")


cfg = r_json(CONFIG_FILE)
STORAGE = {
    "welcome": DEFAULT_WELCOME_PHOTO or cfg.get("welcome") or "",
    "welcome_gif": DEFAULT_WELCOME_GIF or cfg.get("welcome_gif") or "",
    "banner": (os.getenv("BANNER_PHOTO") or PKG_PHOTO).strip(),
    "demos": {int(k): v for k, v in r_json(DEMOS_FILE).items() if str(k).isdigit()},
}

PACKAGES = {
    "file_1": {"name": "01 All mix content VIP Access", "price": 249, "badge": "4̶9̶9̶ ➡️ 💎 ₹249", "emoji": "👑", "link": "https://t.me/+s4Zzmwni59diNjU1"},
    "file_2": {"name": "02 Rap & Big File VD", "price": 89, "badge": "1̶9̶9̶ ➡️ ⚡ ₹89", "emoji": "🔥", "link": "https://t.me/+_AILkUGhVnVkMzBl"},
    "file_3": {"name": "03 Mom and Son Real Sex", "price": 45, "badge": "9̶9̶ ➡️ 🔥 ₹45", "emoji": "💋", "link": "https://t.me/+qjTxEmHC-z4wMzE1"},
    "file_4": {"name": "04 Insta viral reels and sex", "price": 40, "badge": "9̶9̶ ➡️ ✨ ₹40", "emoji": "⚡", "link": "https://t.me/+LmzeU14SK_I0MGY9"},
    "file_5": {"name": "05 Ganga bath group join", "price": 199, "badge": "3̶9̶9̶ ➡️ 👑 ₹199", "emoji": "💎", "link": "https://t.me/+jMs1EZ3RLSc1Yjhl"},
    "file_6": {"name": "06 Bath camera hidden", "price": 55, "badge": "1̶2̶9̶ ➡️ 💥 ₹55", "emoji": "🎥", "link": "https://t.me/+G4yBWASYMzYzOTc9"},
    "file_7": {"name": "07 CP girl real fuke", "price": 65, "badge": "1̶4̶9̶ ➡️ 🌟 ₹65", "emoji": "🌟", "link": "https://t.me/+f9i3BlsoUeZiZmY1"},
    "file_8": {"name": "08 Sister and brother sex", "price": 30, "badge": "7̶9̶ ➡️ 💖 ₹30", "emoji": "💖", "link": "https://t.me/+BYOIdmg4w3c2MjQ1"},
}

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()
loop = asyncio.new_event_loop()
bot_ready = threading.Event()


def _run_bg():
    asyncio.set_event_loop(loop)

    async def _init():
        try:
            await bot_app.initialize()
            await bot_app.start()
            u = (os.getenv("RENDER_EXTERNAL_URL") or "https://viral-content-1bot-1.onrender.com").rstrip("/")
            try:
                await bot_app.bot.set_webhook(f"{u}/{TOKEN}")
            except Exception as e:
                print(f"Hook err: {e}")
        except Exception as e:
            print(f"Init err: {e}")
        finally:
            bot_ready.set()

    loop.run_until_complete(_init())
    loop.run_forever()


threading.Thread(target=_run_bg, daemon=True).start()


def run_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, loop) if bot_ready.wait(timeout=15) else None


def save_cfg():
    w_json(CONFIG_FILE, {"welcome": STORAGE.get("welcome", ""), "welcome_gif": STORAGE.get("welcome_gif", "")})


async def try_del(bot, cid, mid):
    if cid and mid:
        try:
            await bot.delete_message(cid, mid)
        except Exception:
            pass


async def clear_prev(ctx, cid, inc=None):
    await try_del(ctx.bot, cid, ctx.chat_data.pop("last_bot_id", None))
    if inc:
        await try_del(ctx.bot, cid, inc.message_id)


async def send_safe(ctx, cid, photo, cap, kb, video=None, dur=None, anim=None, inc=None):
    await clear_prev(ctx, cid, inc)
    sent = None
    if anim:
        for fn in (
            lambda: ctx.bot.send_animation(cid, anim, caption=cap, reply_markup=kb, parse_mode="Markdown"),
            lambda: ctx.bot.send_video(cid, anim, caption=cap, reply_markup=kb, parse_mode="Markdown", supports_streaming=True),
        ):
            try:
                sent = await fn()
                break
            except BadRequest:
                pass
    if not sent and video:
        try:
            sent = await ctx.bot.send_video(cid, video, caption=cap, reply_markup=kb, parse_mode="Markdown", width=W, height=H, duration=dur, supports_streaming=True)
        except BadRequest:
            pass
    if not sent and photo:
        try:
            if os.path.exists(photo):
                with open(photo, "rb") as fp:
                    sent = await ctx.bot.send_photo(cid, fp, caption=cap, reply_markup=kb, parse_mode="Markdown")
            else:
                sent = await ctx.bot.send_photo(cid, photo, caption=cap, reply_markup=kb, parse_mode="Markdown")
        except BadRequest:
            pass
    if not sent:
        sent = await ctx.bot.send_message(cid, cap, reply_markup=kb, parse_mode="Markdown")
    if sent:
        ctx.chat_data["last_bot_id"] = sent.message_id
    return sent


def make_qr(amt, uid):
    uri = f"upi://pay?pa={UPI_ID}&pn={urllib.parse.quote(BIZ_NAME)}&am={amt}&cu=INR&tn=Order_{uid}"
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
    qr.add_data(uri)
    qr.make(fit=True)
    path = f"qr_{uid}.png"
    qr.make_image(fill_color="black", back_color="white").save(path, optimize=True)
    return path


def menu_kb():
    rows = [[InlineKeyboardButton(f"{p['emoji']} {p['name']} • {p['badge']} 👉", callback_data=k)] for k, p in PACKAGES.items()]
    rows += [[InlineKeyboardButton("🎁 🅵🆁🅴🅴   __   🅳🅴🅼🅾", callback_data="demo_1")], [InlineKeyboardButton("💬 Help & Support", url=SUPPORT_URL)]]
    return InlineKeyboardMarkup(rows)


def reject_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")], [InlineKeyboardButton("💬 Help & Support", url=SUPPORT_URL)]])


async def start(upd: Update, ctx):
    cid = upd.effective_chat.id
    if upd.callback_query:
        await upd.callback_query.answer()
        await try_del(ctx.bot, cid, upd.callback_query.message.message_id)
    gif = STORAGE.get("welcome_gif") or ""
    photo = "" if gif else (STORAGE.get("welcome") or (PKG_PHOTO if os.path.exists(PKG_PHOTO) else ""))
    cap = "❤️ **Welcome to All Max Content Bot!**\n\n🔥 **Special Discount Offer Chal Raha Hai!**\n✅ Direct UPI QR Payment • Fast Approval • Instant Access\n\n👇 Niche se apna package select karein:"
    await send_safe(ctx, cid, photo, cap, menu_kb(), anim=gif or None, inc=upd.message)


async def setwelcome_cmd(upd: Update, ctx):
    if upd.effective_user.id == ADMIN_ID:
        ctx.user_data["pending_welcome"] = True
        await send_safe(ctx, upd.effective_chat.id, "", "🖼️ **Welcome Banner Ready!** 🎞️📸 **GIF** ya **Photo** bhejein.", None, inc=upd.message)


async def setdemo_cmd(upd: Update, ctx):
    if upd.effective_user.id != ADMIN_ID:
        return
    args = ctx.args or []
    if not args or not re.fullmatch(r"\d{1,2}", args[0]):
        await send_safe(ctx, upd.effective_chat.id, "", "⚠️ Use: `/setdemo 1` (1-10)", None, inc=upd.message)
        return
    idx = max(1, min(10, int(args[0])))
    ctx.user_data["pending_demo"] = {"idx": idx, "note": " ".join(args[1:]).strip()}
    await send_safe(ctx, upd.effective_chat.id, "", f"🎬 **Demo {idx} Ready!** 🎥 Video ya photo bhejein.", None, inc=upd.message)


async def deldemo_cmd(upd: Update, ctx):
    if upd.effective_user.id != ADMIN_ID:
        return
    args = ctx.args or []
    demos = STORAGE.setdefault("demos", {})
    if args and args[0].lower() == "all":
        demos.clear()
        w_json(DEMOS_FILE, demos)
        await send_safe(ctx, upd.effective_chat.id, "", "🗑️ **Saare demos delete ho gaye!**", None, inc=upd.message)
        return
    if not args or not re.fullmatch(r"\d{1,2}", args[0]):
        await send_safe(ctx, upd.effective_chat.id, "", "⚠️ Use: `/deldemo 1` ya `/deldemo all`", None, inc=upd.message)
        return
    idx = max(1, min(10, int(args[0])))
    if demos.pop(idx, None) is not None:
        w_json(DEMOS_FILE, demos)
        txt = f"🗑️ **Demo {idx} delete ho gaya!**"
    else:
        txt = f"ℹ️ Demo {idx} khali hai."
    await send_safe(ctx, upd.effective_chat.id, "", txt, None, inc=upd.message)


async def demos_status(upd: Update, ctx):
    if upd.effective_user.id != ADMIN_ID:
        return
    demos = STORAGE.get("demos", {})
    if not demos:
        await send_safe(ctx, upd.effective_chat.id, "", "ℹ️ Koi demo set nahi hai. `/setdemo 1` bhejein.", None, inc=upd.message)
        return
    lines = ["🎬 **Saved Demos (1-10):**"] + [f"• #{i} ({'Video' if demos[i].get('video') else 'Photo'}): {demos[i].get('note', '')}" for i in sorted(demos)]
    await send_safe(ctx, upd.effective_chat.id, "", "\n".join(lines), None, inc=upd.message)


def save_demo(ctx, cap, payload):
    p = ctx.user_data.get("pending_demo")
    m = re.match(r"^/setdemo\s+(\d{1,2})(?:\s+(.*))?$", cap, flags=re.IGNORECASE | re.DOTALL)
    if not (m or p):
        return None
    ctx.user_data.pop("pending_demo", None)
    idx = max(1, min(10, int(m.group(1)))) if m else int(p["idx"])
    note = (m.group(2) or "").strip() if m else (cap or p.get("note") or "")
    STORAGE.setdefault("demos", {})[idx] = dict(payload, note=note)
    w_json(DEMOS_FILE, STORAGE["demos"])
    return idx


async def _save_w_gif(upd: Update, ctx, fid: str):
    STORAGE["welcome_gif"], STORAGE["welcome"] = fid, ""
    save_cfg()
    await send_safe(ctx, upd.effective_chat.id, "", f"✅ **Welcome GIF save ho gaya!** 🎞️\n\n`{fid}`", None, anim=fid, inc=upd.message)


async def on_animation(upd: Update, ctx):
    msg = upd.message
    if msg and msg.animation and upd.effective_user.id == ADMIN_ID:
        if ctx.user_data.get("pending_welcome") or "setwelcome" in (msg.caption or "").lower():
            ctx.user_data.pop("pending_welcome", None)
            await _save_w_gif(upd, ctx, msg.animation.file_id)


async def on_document(upd: Update, ctx):
    msg = upd.message
    if not msg or not msg.document or upd.effective_user.id != ADMIN_ID:
        return
    doc = msg.document
    is_gif = (doc.mime_type or "").lower() == "image/gif" or (doc.file_name or "").lower().endswith(".gif")
    if is_gif and (ctx.user_data.get("pending_welcome") or "setwelcome" in (msg.caption or "").lower()):
        ctx.user_data.pop("pending_welcome", None)
        await _save_w_gif(upd, ctx, doc.file_id)


async def on_video(upd: Update, ctx):
    msg = upd.message
    if not msg or not msg.video or upd.effective_user.id != ADMIN_ID:
        return
    cap = (msg.caption or "").strip()
    if ctx.user_data.get("pending_welcome") or "setwelcome" in cap.lower():
        ctx.user_data.pop("pending_welcome", None)
        await _save_w_gif(upd, ctx, msg.video.file_id)
        return
    idx = save_demo(ctx, cap, {"video": msg.video.file_id, "duration": msg.video.duration})
    if idx:
        await send_safe(ctx, upd.effective_chat.id, "", f"✅ **Demo {idx} (Video) save ho gaya!** 🎬", None, inc=msg)


async def on_photo(upd: Update, ctx):
    msg = upd.message
    if not msg or not msg.photo:
        return
    cid, cap = upd.effective_chat.id, (msg.caption or "").strip()
    if upd.effective_user.id == ADMIN_ID:
        fid = msg.photo[-1].file_id
        if ctx.user_data.get("pending_welcome") or "setwelcome" in cap.lower():
            ctx.user_data.pop("pending_welcome", None)
            STORAGE["welcome"], STORAGE["welcome_gif"] = fid, ""
            save_cfg()
            await send_safe(ctx, cid, fid, f"✅ **Welcome photo save ho gaya!** 🖼️\n\n`{fid}`", None, inc=msg)
            return
        idx = save_demo(ctx, cap, {"photo": fid})
        if idx:
            await send_safe(ctx, cid, "", f"✅ **Demo {idx} (Photo) save ho gaya!** 💾", None, inc=msg)
            return

    pkg_key, uid_obj, now = ctx.user_data.get("qr_pkg"), msg.photo[-1].file_unique_id, time.time()
    for k in [k for k, ts in USED_SS.items() if now - ts >= 86400]:
        del USED_SS[k]
    if not pkg_key or pkg_key not in PACKAGES or uid_obj in USED_SS or getattr(msg, "forward_date", None):
        lbl = f"📦 {PACKAGES[pkg_key]['name']}\n\n" if pkg_key in PACKAGES else ""
        await send_safe(ctx, cid, "", f"❌ **Payment Rejected**\n{lbl}📸 Sahi QR screenshot bhejein ya support karein. 💬", reject_kb(), inc=msg)
        return

    USED_SS[uid_obj] = now
    ctx.user_data.pop("qr_pkg", None)
    pkg, user = PACKAGES[pkg_key], upd.effective_user
    await send_safe(ctx, cid, "", f"⏳ **Screenshot Received!**\n📦 {pkg['name']}\n💰 {pkg['badge']}\n\n✅ Approve hote hi **VIP Link** yahin aayega. 🚀", None, inc=msg)
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{pkg_key}"), InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}_{pkg_key}")]])
    await ctx.bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=f"📥 **Proof**\n👤 {user.full_name} (`{user.id}`)\n📦 {pkg['name']} • **{pkg['badge']}**", reply_markup=kb, parse_mode="Markdown")


async def on_callback(upd: Update, ctx):
    q = upd.callback_query
    await q.answer()
    data, uid, cid = q.data, q.from_user.id, q.message.chat_id
    await try_del(ctx.bot, cid, q.message.message_id)

    if data == "main_menu":
        await start(upd, ctx)
    elif data == "ss_guide":
        await send_safe(ctx, cid, "", "📸 **Screenshot Yahin Bhejein!**\n\n✅ Seedha is chat mein photo bhejein.\n🚀 Approve hote hi **VIP Access Link** yahin aayega.", InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]]))
    elif data.startswith(("approve_", "reject_")) and uid == ADMIN_ID:
        act, tid, key = data.split("_", 2)
        pkg = PACKAGES.get(key, PACKAGES["file_1"])
        if act == "approve":
            await ctx.bot.send_message(int(tid), f"✅ **Payment Approved!** 🎉\n📦 {pkg['name']}\n💰 {pkg['badge']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔓 Access VIP Link 🚀", url=pkg["link"])]]), parse_mode="Markdown")
        else:
            await ctx.bot.send_message(int(tid), f"❌ **Payment Rejected**\n📦 {pkg['name']}\n\n📸 Sahi screenshot bhejein ya support karein. 💬", reply_markup=reject_kb(), parse_mode="Markdown")
    elif data.startswith("demo_"):
        idx = max(1, min(10, int(data.replace("demo_", "") or 1)))
        row = ([InlineKeyboardButton("⬅️ Prev Clip", callback_data=f"demo_{idx - 1}")] if idx > 1 else []) + ([InlineKeyboardButton("Next Clip ➡️", callback_data=f"demo_{idx + 1}")] if idx < 10 else [])
        rows = ([row] if row else []) + ([[InlineKeyboardButton("👑 Get Full VIP Access • 4̶9̶9̶ ➡️ 💎 ₹249", callback_data="file_1")]] if idx == 10 else []) + [[InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")], [InlineKeyboardButton("🎬 Join Demo 2", url=DEMO_URL)]]
        item = STORAGE.get("demos", {}).get(idx, {})
        line = (item.get("note") or "").strip()
        cap = f"✨ **Preview ({idx}/10)** ✨\n\n👑 **Poore Full Access Plan par aapko sab kuch ek saath mil jaayega!** 💎" + (f"\n🔥 {line} 🚀" if line else "")
        fb = PKG_PHOTO if os.path.exists(PKG_PHOTO) else STORAGE.get("banner", "")
        await send_safe(ctx, cid, item.get("photo") or (fb if not item.get("video") else ""), cap, InlineKeyboardMarkup(rows), video=item.get("video"), dur=item.get("duration"))
    elif data in PACKAGES:
        pkg, banner = PACKAGES[data], STORAGE.get("banner") or (PKG_PHOTO if os.path.exists(PKG_PHOTO) else "")
        text = f"💎 **Selected Plan:** {pkg['name']} {pkg['emoji']}\n💰 **Offer Price:** {pkg['badge']}\n\n🛡️ **How it works:**\n1️⃣ ⚡ **Pay Now** dabakar QR code generate karein.\n2️⃣ 📱 UPI se **₹{pkg['price']}** pay karke **screenshot** bhejein.\n3️⃣ 🚀 Verification ke baad **VIP Access Link** yahin mil jaayega."
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(f"⚡ Pay Now • {pkg['badge']}", callback_data=f"pay_{data}")], [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]])
        await send_safe(ctx, cid, banner, text, kb)
    elif data.startswith("pay_"):
        pkg = PACKAGES.get(data.replace("pay_", ""))
        if not pkg:
            return
        ctx.user_data["qr_pkg"] = data.replace("pay_", "")
        qr_path = make_qr(pkg["price"], uid)
        try:
            await clear_prev(ctx, cid)
            cap = f"📱 **SCAN & PAY**\n💎 {pkg['name']} {pkg['emoji']}\n💰 {pkg['badge']}\n\n1️⃣ 📷 QR scan karke **₹{pkg['price']}** pay karein (`{UPI_ID}`).\n2️⃣ 📸 Payment ke baad **yahin** screenshot bhejein.\n3️⃣ 🚀 Approve hote hi **VIP Link** yahin mil jaayega."
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("📸 Send Screenshot Here", callback_data="ss_guide")], [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]])
            with open(qr_path, "rb") as f:
                sent = await ctx.bot.send_photo(cid, f, caption=cap, reply_markup=kb, parse_mode="Markdown")
            if sent:
                ctx.chat_data["last_bot_id"] = sent.message_id
        finally:
            if os.path.exists(qr_path):
                os.remove(qr_path)


for c, h in [("start", start), ("setwelcome", setwelcome_cmd), ("setdemo", setdemo_cmd), ("deldemo", deldemo_cmd), ("demos", demos_status)]:
    bot_app.add_handler(CommandHandler(c, h))
bot_app.add_handler(CallbackQueryHandler(on_callback))
for flt, h in [(filters.ANIMATION, on_animation), (filters.Document.ALL, on_document), (filters.VIDEO, on_video), (filters.PHOTO, on_photo)]:
    bot_app.add_handler(MessageHandler(flt, h))


@app.route("/")
def home():
    return "OK", 200


@app.route("/refresh")
def refresh_hook():
    if bot_ready.is_set():
        u = (os.getenv("RENDER_EXTERNAL_URL") or "https://viral-content-1bot-1.onrender.com").rstrip("/")
        asyncio.run_coroutine_threadsafe(bot_app.bot.set_webhook(f"{u}/{TOKEN}"), loop)
    return "Webhook Refreshed", 200


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        p = request.get_json(force=True, silent=True)
        if p:
            fut = run_async(bot_app.process_update(Update.de_json(p, bot_app.bot)))
            if fut:
                fut.result(timeout=15)
    except Exception as e:
        print(f"Update err: {e}")
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
        
