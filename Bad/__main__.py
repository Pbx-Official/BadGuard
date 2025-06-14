import asyncio
import importlib

import nest_asyncio
from pyrogram import idle
from Bad import LOGGER, HELPABLE, app, Bad, application
from Bad.misc import sudo
from Bad.plugins import ALL_MODULES
from Bad.database.database import get_banned_users, get_gbanned
from config import BANNED_USERS

nest_asyncio.apply()

async def init():
    sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("Bad.plugins").info("Successfully Imported All Modules ")
    
    await Bad.start()
    await application.run_polling()
    await application.start()
    LOGGER("Bad").info("bot start")
    await idle()
    await app.stop()
    await Bad.disconnect()
    await application.shutdown()
    await userbot.stop()
    LOGGER("Bad").info("Stopping Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
  
