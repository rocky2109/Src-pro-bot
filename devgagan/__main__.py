import asyncio
import importlib
import gc
from pyrogram import idle
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from devgagan import app  # ✅ Import app instance
from aiojobs import create_scheduler

loop = asyncio.get_event_loop()

async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(60)
        gc.collect()

async def devggn_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)

    print("""
---------------------------------------------------
📂 Bot Deployed successfully ...
📝 Description: A Pyrogram bot for downloading files from Telegram channels or groups 
                and uploading them back to Telegram.
👨‍💻 Author: Gagan
🌐 GitHub: https://github.com/devgaganin/
📬 Telegram: https://t.me/team_spy_pro
▶️ YouTube: https://youtube.com/@dev_gagan
🗓️ Created: 2025-01-11
🔄 Last Modified: 2025-01-11
🛠️ Version: 2.0.5
📜 License: MIT License
---------------------------------------------------
""")

    # ✅ Send "Bot is live" message to bot's own PM
    try:
        me = await app.get_me()
        await app.send_message(
            chat_id=me.id,
            text="✅ **Bot is now LIVE!**\n\n🧠 Ready to save restricted content.\n⚓ Powered by @Real_Pirates"
        )
        print("✅ Startup message sent to bot's PM.")
    except Exception as e:
        print(f"❌ Failed to send startup PM: {e}")

    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")
    await idle()
    print("Bot stopped...")

if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())
