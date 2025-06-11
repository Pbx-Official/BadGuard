import asyncio
import time
import random

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

import config
from config import BANNED_USERS, START_IMG_URL
from Bad import app
from Bad.misc import SUDOERS, _boot_
from Bad.database.database import (
    add_served_chat,
    add_served_user,
    is_banned_user,
    is_on_off,
    is_served_private_chat,
)
from Bad.database.Buttons import alive_panel, start_pannel
from .help import paginate_modules

STICKER = [
    "CAACAgUAAx0CepnpNQABATUjZypavrymDoERINkF-M3u9JDQ6K8AAhoDAAIOnnlVpyrYiDnVgWYeBA",
]

@app.on_message(group=-1)
async def ban_new(client, message):
    user_id = (
        message.from_user.id if message.from_user and message.from_user.id else 777000
    )
    if await is_banned_user(user_id):
        try:
            alert_message = "😳"
            await message.chat.ban_member(user_id)
            await message.reply_text(alert_message)
        except:
            pass

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
async def start_comm(client, message: Message):
    chat_id = message.chat.id
    await add_served_user(message.from_user.id)
    await message.react("❤️")

    try:
        out = start_pannel({})
        bad = await message.reply_text("**ʜᴇʏ 💌**")
        await bad.delete()
        bad = await message.reply_text("**ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ 💞**")
        await asyncio.sleep(0.1)
        await bad.delete()
        umm = await bad.reply_sticker(sticker=random.choice(STICKER))
        chat_photo = START_IMG_URL
        await umm.delete()

        await message.reply_photo(
            photo=chat_photo,
            caption="Welcome to the bot! I'm here to assist you.",
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} has started bot.\n\n**User ID:** {sender_id}\n**User Name:** {sender_name}",
            )
    except Exception as e:
        print(f"Error: {e}")

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
async def testbot(client, message: Message):
    try:
        chat_id = message.chat.id
        try:
            groups_photo = await client.download_media(
                message.chat.photo.big_file_id, file_name=f"chatpp{chat_id}.png"
            )
            chat_photo = groups_photo if groups_photo else START_IMG_URL
        except AttributeError:
            chat_photo = START_IMG_URL

        out = alive_panel({})
        uptime = int(time.time() - _boot_)

        await message.reply_photo(
            photo=chat_photo,
            caption=f"Bot is alive! Uptime: {get_readable_time(uptime)}",
            reply_markup=InlineKeyboardMarkup(out),
        )
        await add_served_chat(chat_id)
    except Exception as e:
        print(f"Error: {e}")

@app.on_message(filters.new_chat_members, group=3)
async def welcome(client, message: Message):
    chat_id = message.chat.id

    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(chat_id):
            await message.reply_text(
                "**This bot's private mode is enabled. Only my owner can use this. If you want to use it in your chat, ask my owner to authorize your chat.**"
            )
            return await client.leave_chat(chat_id)
    else:
        await add_served_chat(chat_id)

    for member in message.new_chat_members:
        try:
            if member.id == client.id:
                try:
                    groups_photo = await client.download_media(
                        message.chat.photo.big_file_id, file_name=f"chatpp{chat_id}.png"
                    )
                    chat_photo = groups_photo if groups_photo else START_IMG_URL
                except AttributeError:
                    chat_photo = START_IMG_URL

                out = start_pannel()
                await message.reply_photo(
                    photo=chat_photo,
                    caption="Thanks for adding me to the group!",
                    reply_markup=InlineKeyboardMarkup(out),
                )

            if member.id in config.OWNER_ID:
                await message.reply_text(
                    f"Welcome, {client.mention}! The owner {member.mention} has joined!"
                )
            elif member.id in SUDOERS:
                await message.reply_text(
                    f"Welcome, {client.mention}! Sudo user {member.mention} has joined!"
                )
        except Exception as e:
            print(f"Error: {e}")

@app.on_callback_query(filters.regex("go_to_start"))
async def go_to_home(client, callback_query: CallbackQuery):
    out = start_pannel({})
    await callback_query.message.edit_text(
        text=f"Welcome back to the bot, {callback_query.message.from_user.mention}!",
        reply_markup=InlineKeyboardMarkup(out),
    )


__MODULE__ = "ʙᴏᴛ"
__HELP__ = f"""
<b>✦ c sᴛᴀɴᴅs ғᴏʀ ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ.</b>

<b>★ /stats</b> - Gᴇᴛ Tᴏᴘ 𝟷𝟶 Tʀᴀᴄᴋs Gʟᴏʙᴀʟ Sᴛᴀᴛs, Tᴏᴘ 𝟷𝟶 Usᴇʀs ᴏғ ʙᴏᴛ, Tᴏᴘ 𝟷𝟶 Cʜᴀᴛs ᴏɴ ʙᴏᴛ, Tᴏᴘ 𝟷𝟶 Pʟᴀʏᴇᴅ ɪɴ ᴀ ᴄʜᴀᴛ ᴇᴛᴄ ᴇᴛᴄ.

<b>★ /sudolist</b> - Cʜᴇᴄᴋ Sᴜᴅᴏ Usᴇʀs ᴏғ Bᴏᴛ

<b>★ /lyrics [Mᴜsɪᴄ Nᴀᴍᴇ]</b> - Sᴇᴀʀᴄʜᴇs Lʏʀɪᴄs ғᴏʀ ᴛʜᴇ ᴘᴀʀᴛɪᴄᴜʟᴀʀ Mᴜsɪᴄ ᴏɴ ᴡᴇʙ.

<b>★ /song [Tʀᴀᴄᴋ Nᴀᴍᴇ] ᴏʀ [YT Lɪɴᴋ]</b> - Dᴏᴡɴʟᴏᴀᴅ ᴀɴʏ ᴛʀᴀᴄᴋ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ɪɴ ᴍᴘ𝟹 ᴏʀ ᴍᴘ𝟺 ғᴏʀᴍᴀᴛs.

<b>★ /player</b> - Gᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ Pʟᴀʏɪɴɢ Pᴀɴᴇʟ.

<b>★ /queue ᴏʀ /cqueue</b> - Cʜᴇᴄᴋ Qᴜᴇᴜᴇ Lɪsᴛ ᴏғ Mᴜsɪᴄ.

    <u><b>⚡️Pʀɪᴠᴀᴛᴇ Bᴏᴛ:</b></u>
      
<b>✧ /authorize [CHAT_ID]</b> - Aʟʟᴏᴡ ᴀ ᴄʜᴀᴛ ғᴏʀ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ.

<b>✧ /unauthorize[CHAT_ID]</b> - Dɪsᴀʟʟᴏᴡ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ.

<b>✧ /authorized</b> - Cʜᴇᴄᴋ ᴀʟʟ ᴀʟʟᴏᴡᴇᴅ ᴄʜᴀᴛs ᴏғ ʏᴏᴜʀ ʙᴏᴛ.
"""
