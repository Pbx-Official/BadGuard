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

# Helper function for uptime
def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        up_time += str(time_list[i]) + time_suffix_list[i]
    return up_time[::-1]


STICKER = [
    "CAACAgUAAx0CepnpNQABATUjZypavrymDoERINkF-M3u9JDQ6K8AAhoDAAIOnnlVpyrYiDnVgWYeBA",
]

@app.on_message(group=-1)
async def ban_new(client, message):
    user_id = (
        message.from_user.id if message.from_user and message.from_user.id else 777000
    )
    chat_name = message.chat.title if message.chat.title else ""
    if await is_banned_user(user_id):
        try:
            alert_message = f"😳"
            BAN = await message.chat.ban_member(user_id)
            if BAN:
                await message.reply_text(alert_message)
        except:
            pass


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
async def testbot(client, message: Message):
    try:
        chat_id = message.chat.id
        try:
            # Try downloading the group's photo
            groups_photo = await client.download_media(
                message.chat.photo.big_file_id, file_name=f"chatpp{chat_id}.png"
            )
            chat_photo = groups_photo if groups_photo else START_IMG_URL
        except AttributeError:
            # If there's no chat photo, use the default image
            chat_photo = START_IMG_URL

        # Get the alive panel and uptime
        out = alive_panel({})
        uptime = int(time.time() - _boot_)

        # Hardcoded caption
        caption_text = (
            f"{client.mention} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ.\n\n"
            f"<b>✫ ᴜᴘᴛɪᴍᴇ :</b> {get_readable_time(uptime)}"
        )

        # Send the response with the group photo or fallback to START_IMG_URL
        await message.reply_photo(
            photo=chat_photo,
            caption=caption_text,
            reply_markup=InlineKeyboardMarkup(out),
        )

        # Add the chat to the served chat list
        await add_served_chat(chat_id)

    except Exception as e:
        print(f"Error: {e}")

@app.on_message(filters.new_chat_members, group=3)
async def welcome(client, message: Message):
    chat_id = message.chat.id

    # Private bot mode check
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(chat_id):
            await message.reply_text(
                "**ᴛʜɪs ʙᴏᴛ's ᴘʀɪᴠᴀᴛᴇ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ. ᴏɴʟʏ ᴍʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs. ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ, ᴛʜᴇɴ ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ᴏʀ ɢᴇᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ.**"
            )
            return await client.leave_chat(chat_id)
    else:
        await add_served_chat(chat_id)

    for member in message.new_chat_members:
        try:
            # If bot itself joins the chat
            if member.id == client.id:
                try:
                    groups_photo = await client.download_media(
                        message.chat.photo.big_file_id, file_name=f"chatpp{chat_id}.png"
                    )
                    chat_photo = groups_photo if groups_photo else START_IMG_URL
                except AttributeError:
                    chat_photo = START_IMG_URL

                out = start_pannel({})
                await message.reply_photo(
                    photo=chat_photo,
                    caption="**๏ ᴛʜɪs ɪs ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs + ᴄʜᴀɴɴᴇʟs ᴠᴄ.**\n\n**🎧 ᴘʟᴀʏ + ᴠᴘʟᴀʏ + ᴄᴘʟᴀʏ + ᴄᴠᴘʟᴀʏ 🎧**\n\n**➥ sᴜᴘᴘᴏʀᴛᴇᴅ ᴡᴇʟᴄᴏᴍᴇ - ʟᴇғᴛ ɴᴏᴛɪᴄᴇ, ᴛᴀɢᴀʟʟ, ᴠᴄᴛᴀɢ, ʙᴀɴ - ᴍᴜᴛᴇ, sʜᴀʏʀɪ, ʟᴜʀɪᴄs, sᴏɴɢ - ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅ, ᴇᴛᴄ... **\n\n**🔐ᴜꜱᴇ » /help ᴛᴏ ᴄʜᴇᴄᴋ ғᴇᴀᴛᴜʀᴇs.** 💞",
                    reply_markup=InlineKeyboardMarkup(out),
                )

            # Owner joined
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    f"ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ {client.mention}, {member.mention} ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ᴄʜᴀᴛ."
                )

            # SUDOERS joined
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"ᴛʜᴇ sᴜᴅᴏ ᴜsᴇʀ ᴏғ {client.mention}, {member.mention} ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ᴄʜᴀᴛ."
                )
            return

        except Exception as e:
            print(f"Error: {e}")
            return

@app.on_callback_query(filters.regex("go_to_start"))
async def go_to_home(client, callback_query: CallbackQuery):
    out = start_pannel({})
    await callback_query.message.edit_text(
        text="**๏ ᴛʜɪs ɪs ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs + ᴄʜᴀɴɴᴇʟs ᴠᴄ.**\n\n**🎧 ᴘʟᴀʏ + ᴠᴘʟᴀʏ + ᴄᴘʟᴀʏ + ᴄᴠᴘʟᴀʏ 🎧**\n\n**➥ sᴜᴘᴘᴏʀᴛᴇᴅ ᴡᴇʟᴄᴏᴍᴇ - ʟᴇғᴛ ɴᴏᴛɪᴄᴇ, ᴛᴀɢᴀʟʟ, ᴠᴄᴛᴀɢ, ʙᴀɴ - ᴍᴜᴛᴇ, sʜᴀʏʀɪ, ʟᴜʀɪᴄs, sᴏɴɢ - ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅ, ᴇᴛᴄ... **\n\n**🔐ᴜꜱᴇ » /help ᴛᴏ ᴄʜᴇᴄᴋ ғᴇᴀᴛᴜʀᴇs.** 💞",
        reply_markup=InlineKeyboardMarkup(out),
    )

__MODULE__ = "ʙᴏᴛ"
__HELP__ = f"""
<b>✦ c sᴛᴀɴᴅs ғᴏʀ ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ.</b>

<b>★ /stats</b> - Gᴇᴛ Tᴏᴘ 𝟷𝟶 Tʀᴀᴄᴋs Gʟᴏʙᴀʟ Sᴛᴀᴛs, Tᴏᴘ 𝟷𝟶 Usᴇʀs ᴏғ ʙᴏᴛ, Tᴏᴘ 𝟷𝟶 Cʜᴀᴛs ᴏɴ ʙᴏᴛ, Tᴏᴘ 𝟷𝟶 Pʟᴀʏᴇʀs ᴏɴ ʙᴏᴛ.

<b>★ /sudolist</b> - Cʜᴇᴄᴋ Sᴜᴅᴏ Usᴇʀs ᴏғ Bᴏᴛ

<b>★ /lyrics [Mᴜsɪᴄ Nᴀᴍᴇ]</b> - Sᴇᴀʀᴄʜᴇs Lʏʀɪᴄs ғᴏʀ ᴛʜᴇ ᴘᴀʀᴛɪᴄᴜʟᴀʀ Mᴜsɪᴄ ᴏɴ ᴡᴇʙ.

<b>★ /song [Tʀᴀᴄᴋ Nᴀᴍᴇ] ᴏʀ [YT Lɪɴᴋ]</b> - Dᴏᴡɴʟᴏᴀᴅ ᴀɴʏ ᴛʀᴀᴄᴋ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ɪɴ ᴍᴘ𝟹 ᴏʀ ᴍᴘ𝟷 ғᴏʀᴍᴀᴛs.

<b>★ /player</b> - Gᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ Pʟᴀʏɪɴɢ Pᴀɴᴇʟ.

<b>★ /queue ᴏʀ /cqueue</b> - Cʜᴇᴄᴋ Qᴜᴇᴜᴇ Lɪsᴛ ᴏғ Mᴜsɪᴄ.

    <u><b>⚡️Pʀɪᴠᴀᴛᴇ Bᴏᴛ:</b></u>
      
<b>✧ /authorize [CHAT_ID]</b> - Aʟʟᴏᴡ ᴀ ᴄʜᴀᴛ ғᴏʀ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ.

<b>✧ /unauthorize[CHAT_ID]</b> - Dɪsᴀʟʟᴏᴡ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ.

<b>✧ /authorized</b> - Cʜᴇᴄᴋ ᴀʟʟ ᴀʟʟᴏᴡᴇᴅ ᴄʜᴀᴛs ᴏғ ʏᴏᴜʀ ʙᴏᴛ.
"""
