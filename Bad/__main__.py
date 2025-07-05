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
    except Exception as e:
        LOGGER(__name__).error(f"Error loading banned users: {e}")
    
    await app.start()
    
    loaded_plugins = []
    for all_module in ALL_MODULES:
        try:
            imported_module = importlib.import_module(all_module)
            if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
                loaded_plugins.append(imported_module.__MODULE__)
                if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                    HELPABLE[imported_module.__MODULE__.lower()] = imported_module
        except Exception as e:
            LOGGER(__name__).error(f"Error importing module {all_module}: {e}")
    
    LOGGER("Bad.plugins").info(f"Successfully Imported Modules: {', '.join(loaded_plugins)}")
    
    await Bad.start()
    await application.run_polling()
    await application.start()
    LOGGER("Bad").info("Bot started")
    await idle()
    await app.stop()
    await Bad.disconnect()
    await application.shutdown()
    LOGGER("Bad").info("Stopping Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
