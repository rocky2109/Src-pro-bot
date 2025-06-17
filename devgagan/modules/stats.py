# ---------------------------------------------------
# File Name: stats.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------


import os
import time
import sys
import motor
from devgagan import app
from pyrogram import filters
from config import OWNER_ID
from devgagan.core.mongo.users_db import get_users, add_user, get_user
from devgagan.core.mongo.plans_db import premium_users
from pyrogram.types import Message

@app.on_message(filters.command("id"))
async def id_command(client, message: Message):
    reply = message.reply_to_message

    user = reply.from_user if reply else message.from_user
    user_id = user.id if user else "N/A"
    chat_id = message.chat.id
    msg_id = message.id
    reply_id = reply.message_id if reply else "N/A"

    text = (
        f"👤 User ID: `{user_id}`\n"
        f"💬 Chat ID: `{chat_id}`\n"
        f"📎 Message ID: `{msg_id}`\n"
        f"🔁 Reply to Msg ID: `{reply_id}`"
    )

    await message.reply_text(text, quote=True)


start_time = time.time()

@app.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        if message.from_user:
            us_in_db = await get_user(message.from_user.id)
            if not us_in_db:
                await add_user(message.from_user.id)
    except:
        pass



def time_formatter():
    minutes, seconds = divmod(int(time.time() - start_time), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if tmp != "":
        if tmp.endswith(":"):
            return tmp[:-1]
        else:
            return tmp
    else:
        return "0 s"


@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    start = time.time()
    users = len(await get_users())
    premium = await premium_users()
    ping = round((time.time() - start) * 1000)
    await message.reply_text(f"""
**Stats of** {(await client.get_me()).mention} :

🏓 **Ping Pong**: {ping}ms

📊 **Total Users** : `{users}`
📈 **Premium Users** : `{len(premium)}`
⚙️ **Bot Uptime** : `{time_formatter()}`
    
🎨 **Python Version**: `{sys.version.split()[0]}`
📑 **Mongo Version**: `{motor.version}`
""")

@app.on_message(filters.command("getusers") & filters.user(OWNER_ID))
async def get_all_users(client, message: Message):
    users = await get_users()

    if not users:
        return await message.reply("🚫 No users found in the database.")

    lines = []
    for uid in users:
        try:
            user = await client.get_users(uid)
            mention = user.mention
        except:
            mention = f"`{uid}`"
        lines.append(f"• {mention} — `{uid}`")

    text = "\n".join(lines)

    if len(text) < 4096:
        await message.reply_text(f"👥 **All Users of the Bot**:\n\n{text}")
    else:
        with open("users.txt", "w", encoding="utf-8") as f:
            f.write("All Bot Users:\n\n" + text)
        await message.reply_document("users.txt", caption="📋 All Users List")
        os.remove("users.txt")
