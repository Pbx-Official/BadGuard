from pyrogram import filters, enums
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)
import requests
from Pbx import Owner
from Bad import app
from Bad.misc import SUDOERS
from pyrogram.errors import UserNotParticipant
from config import LOG_GROUP_ID, OWNER_ID
from pyrogram.types import *
from Bad.plugins.Ban import extract_user, mention


async def sban_user(user_id, first_name, admin_id, admin_name, chat_id, reason, message, time=None):
    if user_id in Owner:
        msg_text = "ꜱᴏʀʀʏ ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴍʏ ʙᴇꜱᴛꜰʀɪᴇɴᴅ .."
        return msg_text, False
    try:
        member = await app.get_chat_member(chat_id, user_id)
        if member.status == enums.ChatMemberStatus.BANNED:
            return "ɪ ᴛʜɪɴᴋ ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ .", False


        await app.ban_chat_member(chat_id, user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
        else:
             pass

        url = "https://api.waifu.pics/sfw/kick"
        user_mention = mention(user_id, first_name)
        admin_mention = mention(admin_id, admin_name)
        button = [
            [
                InlineKeyboardButton(
                    text="ᴜɴʙᴀɴ ",    
                    callback_data=f"unban_={user_id}",
                ),
                InlineKeyboardButton(
                    text="ᴄʟᴏꜱᴇ",
                    callback_data=f"close",
                ),
            ]
        ]
        response = requests.get(url).json()
        pimg = response['url']
        await app.send_message(LOG_GROUP_ID, f"{user_mention} sbanned by {admin_mention} in {message.chat.title}")
        result_msg = await message.reply_video(
            pimg,
            caption=f"<u>ѕʙᴀɴ ᴇᴠᴇɴᴛ ❗ </u> \n\nɴᴀᴍᴇ - {user_mention}\nʙᴀɴɴᴇᴅ ʙʏ - {admin_mention}\n",
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


@app.on_message(filters.command(["sban"]))
async def sban_command_handler(client, message):
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

    msg_text, result = await sban_user(user_id, first_name, admin_id, admin_name, chat_id, reason, message)
    if not result:
        await message.reply_text(msg_text)
