from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, MASTER_BOT_TOKEN, OWNER_ID, SUDO_USERS
import database as db

app = Client(
    "master_clone_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=MASTER_BOT_TOKEN
)

# ---------- HELPERS ----------
def is_sudo(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in SUDO_USERS

# ---------- START ----------
@app.on_message(filters.command("start") & filters.private)
async def start(_, m):
    text = (
        "👋 **Welcome to Master Clone Bot**\n\n"
        "Create premium Telegram bots with ease 🚀\n\n"
        "👇 Tap below to start cloning"
    )
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🤖 Clone a Bot", callback_data="clone")]]
    )
    await m.reply(text, reply_markup=buttons)

# ---------- CLONE ----------
@app.on_callback_query(filters.regex("^clone$"))
async def clone_menu(_, q):
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎵 VC Music Bot", callback_data="clone_music")]]
    )
    await q.message.edit("Choose bot type 👇", reply_markup=buttons)

@app.on_callback_query(filters.regex("^clone_music$"))
async def clone_music(_, q):
    text = (
        "🎵 **VC Music Bot**\n\n"
        "💰 **One-time payment required**\n\n"
        "UPI ID: `yourfampay@upi`\n"
        "Amount: ₹149.63 (EXACT)\n\n"
        "After payment, click below 👇"
    )
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✅ I have done payment", callback_data="paid")]]
    )
    await q.message.edit(text, reply_markup=buttons)

# ---------- PAYMENT ----------
@app.on_callback_query(filters.regex("^paid$"))
async def paid_cb(_, q):
    uid = q.from_user.id
    db.users[uid] = {"step": "details"}

    await q.message.edit(
        "📥 **Send details in ONE message:**\n\n"
        "1️⃣ Last 4 digits of TXN ID\n"
        "2️⃣ Exact amount\n"
        "3️⃣ Time (HH:MM)\n"
        "4️⃣ Bot Token"
    )

# ---------- COLLECT DETAILS ----------
@app.on_message(filters.private & filters.text)
async def collect(_, m):
    uid = m.from_user.id

    if uid not in db.users:
        return
    if db.users[uid].get("step") != "details":
        return

    bot_id = f"bot_{len(db.bots) + 1}"

    db.bots[bot_id] = {
        "owner": uid,
        "details": m.text,
        "status": "unverified"
    }

    db.users[uid]["step"] = None

    await m.reply(
        "✅ **Details received!**\n\n"
        "Your bot is ready to use 🚀\n"
        "⏳ Payment will be verified soon.\n\n"
        "If payment is valid → bot stays\n"
        "If not → bot will be deleted ❌"
    )

# ---------- SUDO COMMANDS ----------

@app.on_message(filters.command("pending") & filters.private)
async def pending(_, m):
    if not is_sudo(m.from_user.id):
        return await m.reply("❌ Not authorized.")

    text = "🕒 **Pending (Unverified) Bots:**\n\n"
    found = False

    for bot_id, data in db.bots.items():
        if data["status"] == "unverified":
            found = True
            text += f"• `{bot_id}` | Owner: `{data['owner']}`\n"

    if not found:
        text += "No pending bots."

    await m.reply(text)

@app.on_message(filters.command("verify") & filters.private)
async def verify(_, m):
    if not is_sudo(m.from_user.id):
        return await m.reply("❌ Not authorized.")

    if len(m.command) < 2:
        return await m.reply("Usage:\n/verify <bot_id>")

    bot_id = m.command[1]

    if bot_id not in db.bots:
        return await m.reply("❌ Bot not found.")

    db.bots[bot_id]["status"] = "verified"
    owner = db.bots[bot_id]["owner"]

    await m.reply(f"✅ `{bot_id}` verified successfully.")
    await app.send_message(
        owner,
        "🎉 **Payment verified!**\nYour bot is now permanent 🚀"
    )

# ---------- RUN ----------
print("🤖 Master Clone Bot running...")
app.start()
idle()