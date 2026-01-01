from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, MASTER_BOT_TOKEN
import database as db

app = Client(
    "master_clone_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=MASTER_BOT_TOKEN
)

# /start
@app.on_message(filters.command("start") & filters.private)
async def start(_, m):
    text = (
        "👋 **Welcome to Master Clone Bot**\n\n"
        "I help you create premium Telegram bots\n"
        "with high-quality hosting 🚀\n\n"
        "👇 Start by cloning a bot"
    )
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🤖 Clone a Bot", callback_data="clone")]]
    )
    await m.reply(text, reply_markup=buttons)

# Clone button
@app.on_callback_query(filters.regex("^clone$"))
async def clone_cb(_, q):
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎵 VC Music Bot", callback_data="clone_music")]]
    )
    await q.message.edit(
        "Choose a bot type to clone 👇",
        reply_markup=buttons
    )

# VC Music selected
@app.on_callback_query(filters.regex("^clone_music$"))
async def clone_music(_, q):
    text = (
        "🎵 **VC Music Bot** selected\n\n"
        "💰 **One-time payment required**\n\n"
        "UPI ID: `yourfampay@upi`\n"
        "Amount: ₹149.63 (EXACT)\n\n"
        "After payment, click below 👇"
    )
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✅ I have done payment", callback_data="paid")]]
    )
    await q.message.edit(text, reply_markup=buttons)

# Payment done
@app.on_callback_query(filters.regex("^paid$"))
async def paid_cb(_, q):
    user_id = q.from_user.id
    db.users[user_id] = {"step": "awaiting_details"}

    await q.message.edit(
        "📥 **Send payment details in this format:**\n\n"
        "1️⃣ Last 4 digits of TXN ID\n"
        "2️⃣ Exact amount\n"
        "3️⃣ Time (HH:MM)\n"
        "4️⃣ Bot Token\n\n"
        "**Send all details in ONE message**"
    )

# Collect details
@app.on_message(filters.private & filters.text)
async def collect_details(_, m):
    user_id = m.from_user.id

    if user_id not in db.users:
        return

    if db.users[user_id].get("step") != "awaiting_details":
        return

    details = m.text.strip()
    bot_id = f"bot_{len(db.bots)+1}"

    db.bots[bot_id] = {
        "owner": user_id,
        "details": details,
        "status": "unverified"
    }

    db.users[user_id]["step"] = None

    await m.reply(
        "✅ **Details received!**\n\n"
        "Your bot is being prepared 🚀\n\n"
        "⏳ Payment will be verified soon.\n"
        "If payment is valid → bot stays alive\n"
        "If not → bot will be removed."
    )

print("🤖 Master Clone Bot is running...")
app.start()
idle()