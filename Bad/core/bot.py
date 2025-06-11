from pyrogram import Client as PyrogramClient, errors as pyrogram_errors
from pyrogram.enums import ChatMemberStatus
from telethon import TelegramClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import config
from ..logging import LOGGER

# Shared state to avoid duplicate log messages
class BotState:
    message_already_sent = False

async def send_startup_message(bot_id, bot_name, bot_username, bot_mention):
    if BotState.message_already_sent:
        return

    msg = (
        f"<u><b>» {bot_mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
        f"ɪᴅ : <code>{bot_id}</code>\n"
        f"ɴᴀᴍᴇ : {bot_name}\n"
        f"ᴜsᴇʀɴᴀᴍᴇ : @{bot_username}"
    )

    try:
        # Pyrogram
        if hasattr(config, "pyrogram_bot"):
            await config.pyrogram_bot.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=msg,
            )
        # Telethon
        elif hasattr(config, "telethon_bot"):
            await config.telethon_bot.send_message(
                config.LOG_GROUP_ID,
                msg
            )
        # PTB
        elif hasattr(config, "ptb_bot"):
            await config.ptb_bot.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=msg,
            )
        LOGGER(__name__).info(f"Message sent successfully to LOG_GROUP_ID: {config.LOG_GROUP_ID}")
        BotState.message_already_sent = True
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
        me = await self.get_me()
        self.id = me.id
        self.name = me.first_name + " " + (me.last_name or "")
        self.username = me.username
        self.mention = me.mention

        config.pyrogram_bot = self  # For common sender
        await send_startup_message(self.id, self.name, self.username, self.mention)

        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        LOGGER(__name__).info(f"Bot member status in the group: {a.status}")
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error("Please promote your bot as an admin in your log group/channel.")
            exit()
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

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

        config.telethon_bot = self  # For common sender
        await send_startup_message(self.id, self.name, self.username, self.mention)
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

    config.ptb_bot = bot  # For common sender
    await send_startup_message(bot.id, bot.name, bot.username, bot.mention)

application = ApplicationBuilder().token(config.BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

plugins = dict(root="Bad.plugins")
