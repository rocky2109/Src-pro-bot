import asyncio
import importlib
import gc
from pyrogram import idle
from devgagan import app  # ✅ Make sure 'app' is imported
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from config import LOG_GROUP  # ✅ Must be a valid chat ID (e.g., -100...)

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
...
---------------------------------------------------
""")

    # ✅ Send startup message
    try:
        await app.send_message(
            LOG_GROUP,
            "✅ **Save Restricted Bot is now live!**\n\n⚙️ All systems are online.\n⚓ Powered by @Real_Pirates"
        )
    except Exception as e:
        print(f"❌ Couldn't send bot live message: {e}")

    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")
    await idle()
    print("Bot stopped...")

if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())
