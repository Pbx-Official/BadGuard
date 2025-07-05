from pyrogram import Client as PyrogramClient, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
from telethon import TelegramClient
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
import config
from ..logging import LOGGER
from Bad.plugins import ALL_MODULES

async def send_startup_message(client, client_type: str):
    """Send a single startup message to the log group with loaded plugins."""
    try:
        loaded_plugins = []
        for module in ALL_MODULES:
            try:
                imported_module = importlib.import_module(module)
                if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
                    loaded_plugins.append(imported_module.__MODULE__)
            except Exception as e:
                LOGGER(__name__).error(f"Error importing module {module} for startup message: {e}")
        
        plugins_text = "\n\n**Loaded Plugins:**\n" + "\n".join(f"• {plugin}" for plugin in loaded_plugins) if loaded_plugins else "\n\n**Loaded Plugins:** None"
        
        LOGGER(__name__).info(f"Attempting to send message to LOG_GROUP_ID: {config.LOG_GROUP_ID} using {client_type}")
        await client.send_message(
            chat_id=config.LOG_GROUP_ID,
            text=(
                f"<u><b>» {client.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                f"ɪᴅ : <code>{client.id}</code>\n"
                f"ɴᴀᴍᴇ : {client.name}\n"
                f"ᴜsᴇʀɴᴀᴍᴇ : @{client.username}"
                f"{plugins_text}"
            ),
            parse_mode=ParseMode.HTML
        )
        LOGGER(__name__).info(f"Message sent successfully to LOG_GROUP_ID: {config.LOG_GROUP_ID}")
    except (errors.ChannelInvalid, errors.PeerIdInvalid):
        LOGGER(__name__).error(
            "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
        )
        exit()
    except Exception as ex:
        LOGGER(__name__).error(
            f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}.\nException: {ex}"
        )
        exit()

class jass(PyrogramClient):
    def __init__(self):
        LOGGER(__name__).info("Starting Pyrogram Bot...")
        super().__init__(
            name="jassMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.me = await self.get_me()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        await send_startup_message(self, "Pyrogram")

        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        LOGGER(__name__).info(f"Bot member status in the group: {a.status}")
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()
        LOGGER(__name__).info(f"Pyrogram Bot Started as {self.name}")

    async def stop(self):
        await super().stop()

class Bad(TelegramClient):
    def __init__(self):
        LOGGER(__name__).info("Starting Telethon Bot...")
        super().__init__(
            'telethon_session',
            api_id=config.API_ID,
            api_hash=config.API_HASH
        )

    async def start(self):
        await super().start(bot_token=config.BOT_TOKEN)
        me = await self.get_me()
        self.id = me.id
        self.name = me.first_name + " " + (me.last_name or "")
        self.username = me.username
        self.mention = f"@{self.username}"
        await send_startup_message(self, "Telethon")
        LOGGER(__name__).info(f"Telethon Bot Started as {self.name}")

    async def stop(self):
        await super().stop()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    me = await bot.get_me()
    bot.id = me.id
    bot.name = me.first_name + " " + (me.last_name or "")
    bot.username = me.username
    bot.mention = f"@{bot.username}"
    await send_startup_message(bot, "python-telegram-bot")
    LOGGER(__name__).info(f"python-telegram-bot Started as {bot.name}")

# Initialize the python-telegram-bot application
application = ApplicationBuilder().token(config.BOT_TOKEN).build()
