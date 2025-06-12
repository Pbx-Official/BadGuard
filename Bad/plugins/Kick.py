from pyrogram import filters, enums
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)
import requests
from Pbx import Owner
from Bad import app, LOGGER
from Bad.misc import SUDOERS
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from config import LOG_GROUP_ID, OWNER_ID
from pyrogram.types import *
from traceback import format_exc
from typing import Tuple
from pyrogram.enums import MessageEntityType as entity


def mention(user, name, mention=True):
    if mention:
        link = f"[{name}](tg://openmessage?user_id={user})"
    else:
        link = f"[{name}](https://t.me/{user})"
    return link


async def extract_user(c: app, m: Message) -> Tuple[int, str, str]:
    user_id = None
    first_name = None
    user_name = None

    if m.reply_to_message and m.reply_to_message.from_user:
        user_id = m.reply_to_message.from_user.id
        first_name = m.reply_to_message.from_user.first_name
        user_name = m.reply_to_message.from_user.username

    elif len(m.text.split()) > 1:
        if len(m.entities) > 1:
            required_entity = m.entities[1]
            if required_entity.type == entity.TEXT_MENTION:
                user_id = required_entity.user.id
                first_name = required_entity.user.first_name
                user_name = required_entity.user.username
            elif required_entity.type in (entity.MENTION, entity.PHONE_NUMBER):
                user_found = m.text[
                    required_entity.offset : (
                        required_entity.offset + required_entity.length
                    )
                ]

                try:
                    user_found = int(user_found)
                except (ValueError, Exception) as ef:
                    if "invalid literal for int() with base 10:" in str(ef):
                        user_found = str(user_found)
                    else:
                        LOGGER.error(ef)
                        LOGGER.error(format_exc())

                try:
                    user = await c.get_users(user_found)
                except Exception as ef:
                    try:
                        user_r = await c.resolve_peer(user_found)
                        user = await c.get_users(user_r.user_id)
                    except PeerIdInvalid:
                        return await m.reply_text("ɪ ᴅɪᴅɴ'ᴛ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ")
                    except Exception as ef:
                        return await m.reply_text(f"ɪ ᴅɪᴅɴ'ᴛ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ: {ef}")
                user_id = user.id
                first_name = user.first_name
                user_name = user.username
            else:
                user_id = None
                first_name = None
                user_name = None
                LOGGER.error(ef)
                LOGGER.error(format_exc())
        else:
            try:
                user_id = int(m.text.split()[1])
            except (ValueError, Exception) as ef:
                if "invalid literal for int() with base 10:" in str(ef):
                    user_id = (
                        str(m.text.split()[1])
                        if (m.text.split()[1]).startswith("@")
                        else None
                    )
                else:
                    user_id = m.text.split()[1]
                    LOGGER.error(ef)
                    LOGGER.error(format_exc())

            if user_id is not None:
                try:
                    user = await c.get_users(user_id)
                except Exception as ef:
                    try:
                        user_r = await c.resolve_peer(user_id)
                        user = await c.get_users(user_r.user_id)
                    except PeerIdInvalid:
                        return await m.reply_text("ɪ ᴅɪᴅɴ'ᴛ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ")
                    except Exception as ef:
                        return await m.reply_text(f"ɪ ᴅɪᴅɴ'ᴛ ꜰɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ: {ef}")
                first_name = user.first_name
                user_name = user.username
                LOGGER.error(ef)
                LOGGER.error(format_exc())
    else:
        user_id = m.from_user.id
        first_name = m.from_user.first_name
        user_name = m.from_user.username

    return user_id, first_name, user_name


async def kick_user(user_id, first_name, admin_id, admin_name, chat_id, reason, message, time=None):
    if user_id in Owner:
        msg_text = "ꜱᴏʀʀʏ ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴍʏ ʙᴇꜱᴛꜰʀɪᴇɴᴅ .."
        return msg_text, False
    try:
        member = await app.get_chat_member(chat_id, user_id)
        if member.status == enums.ChatMemberStatus.BANNED:
            return "ɪ ᴛʜɪɴᴋ ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ .", False

        await app.ban_chat_member(chat_id, user_id)
        await app.unban_chat_member(chat_id, user_id)
      

        url = "https://api.waifu.pics/sfw/kick"
        user_mention = mention(user_id, first_name)
        admin_mention = mention(admin_id, admin_name)
        button = [
            [
                
                InlineKeyboardButton(
                    text="ᴄʟᴏꜱᴇ",
                    callback_data=f"close",
                ),
            ]
        ]
        response = requests.get(url).json()
        pimg = response['url']
        await app.send_message(LOG_GROUP_ID, f"{user_mention} kicked by {admin_mention} in {message.chat.title}")
        result_msg = await message.reply_video(
            pimg,
            caption=f"<u>ᴋɪᴄᴋ ᴇᴠᴇɴᴛ ❗ </u> \n\nɴᴀᴍᴇ - {user_mention}\nʙᴀɴɴᴇᴅ ʙʏ - {admin_mention}\n",
            reply_markup=InlineKeyboardMarkup(button)
        )
        
        return result_msg, True
    except ChatAdminRequired:
        msg_text = "ɢɪᴠᴇ ᴍᴇ ʙᴀɴ ʀɪɢʜᴛꜱ ᴛʜᴇɴ ᴜꜱᴇ ɪᴛ."
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "ꜱᴏʀʀʏ ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴀɴ ᴀᴅᴍɪɴ."
        return msg_text, False
    except UserNotParticipant:
        msg = f"ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴀɴ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ᴏꜰ \n{m.chat.title}."
        return msg, False
    except Exception as e:
        await app.send_message(LOG_GROUP_ID, f"An error occurred in Ban - {e}")
        return str(e), False


@app.on_message(filters.command(["kick"]))
async def ban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    if admin_id in Owner:
        pass
    else:
        member = await chat.get_member(admin_id)
        if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
            if member.privileges.can_restrict_members:
                pass
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ.."
                return await message.reply_text(msg_text)
        else:
            msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ."
            return await message.reply_text(msg_text)

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        reason = None
    else:
        user_id, first_name, _ = await extract_user(client, message)
        reason = message.text.partition(message.command[1])[2] if len(message.command) > 1 else None

    if user_id is None:
        return await message.reply_text("User not found!")

    msg_text, result = await ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason, message)
    if not result:
        await message.reply_text(msg_text)


@app.on_message(filters.command("kickme") & filters.group)
async def kickme_command(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    url = f"https://api.waifu.pics/sfw/kick"
    response = requests.get(url).json()
    up = response['url']

    try:
        # kick him
        await app.ban_chat_member(chat_id, user_id)
        # Mention the kicked member in the group
        await message.reply_video(
            up,
            caption=f"Lᴏʟ ! {user_name} ʜᴀs ʙᴇᴇɴ sᴇʟғ ᴋɪᴄᴋᴇᴅ ᴏᴜᴛ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ 🤣 .",
            reply_markup=InlineKeyboardMarkup(button),
        )
        await app.send_message(LOG_GROUP_ID, f"{user_name} used kickme command from {message.chat.title}")
    except Exception as e:
        # Handle any errors that may occur during the kicking process
        await message.reply_text(f"An error occurred: {str(e)}")

