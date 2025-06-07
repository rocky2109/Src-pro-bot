# ---------------------------------------------------
# File Name: __init__.py
# Description: A Pyrogram + Telethon bot for Telegram
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# ---------------------------------------------------

import os
import time
import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from pyrogram.enums import ParseMode
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING, MONGO_DB

# Logging setup
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# Pyrogram bot client
app = Client(
    ":RestrictBot:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    parse_mode=ParseMode.MARKDOWN
)

# Pyrogram userbot client (STRING session)
pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

# Telethon bot client — don't start yet
sex = TelegramClient('sexrepo', API_ID, API_HASH)

# MongoDB setup
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

# TTL Index creation
async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)
    print("✅ MongoDB TTL index created.")

# Main startup logic
async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME

    await create_ttl_index()

    # Start Pyrogram bot
    await app.start()

    # Start Telethon bot
    await sex.start(bot_token=BOT_TOKEN)

    # Get bot info
    me = await app.get_me()
    BOT_ID = me.id
    BOT_USERNAME = me.username
    BOT_NAME = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name

    # Start userbot (optional)
    if STRING:
        await pro.start()

# Run bot with event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(restrict_bot())
