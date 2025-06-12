import random
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, BadRequest
from Bad import app
import requests
from Bad.plugins.Ban import mention, extract_user
from config import OWNER_ID, LOG_GROUP_ID
from Pbx import Owner


async def demote_user(user_id, first_name, admin_id, admin_name, chat_id, message):
    if user_id in Owner:
        return "ᴏʜ ᴍʏ ᴅᴏɢ !", False

    try:
        # Check user status
        user_status = await app.get_chat_member(chat_id, user_id)
        if user_status.status == enums.ChatMemberStatus.OWNER:
            return "ᴍʏ ᴄᴜᴛᴇ ᴍᴀꜱᴛᴇʀ ɪ ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ 😁", False
        if user_status.status not in [enums.ChatMemberStatus.ADMINISTRATOR]:
            return "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ", False

        await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
            can_change_info=False,
            can_invite_users=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=False,
            can_manage_video_chats=False,
        ))
    except ChatAdminRequired as e:
        if "[403 CHAT_ADMIN_REQUIRED]" in str(e):
            return "This user is promoted by others i cant demote him✨.", False
        else:
            return "ꜰɪʀꜱᴛ ɢɪᴠᴇ ᴍᴇ ʀɪɢʜᴛꜱ ᴛʜᴇɴ ᴜꜱᴇ ɪᴛ 🥺", False
    except BadRequest as e:
        if "USER_CREATOR" in str(e):
            return "ᴍʏ ᴄᴜᴛᴇ ᴍᴀꜱᴛᴇʀ ɪ ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ 😠", False
        else:
            await message.reply_text(f"Oh An Error Occurred Please Report it at support chat \n\n Error Type: {e}")

    url = "https://api.waifu.pics/sfw/dance"
    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    button = [
       [
           InlineKeyboardButton(
               text="• ᴅᴇʟᴇᴛᴇ •",
               callback_data="close",
           ),
       ]
    ]
    response = requests.get(url).json()
    pimg = response['url']
    await app.send_message(LOG_GROUP_ID, f"{user_mention} ᴅᴇᴍᴏᴛᴇ Bʏ {admin_mention} in {message.chat.title}")
    promoteee = await message.reply_video(
        video=pimg,
        caption=f"<u>ᴅᴇᴍᴏᴛᴇ Eᴠᴇɴᴛ🚫</u> \n\n ɴᴀᴍᴇ - {user_mention}\n ᴅᴇᴍᴏᴛᴇ Bʏ - {admin_mention}\n",
        reply_markup=InlineKeyboardMarkup(button)
    )

    return promoteee, True


@app.on_message(filters.command(["Demote"]) & filters.group)
async def cutexdemotes(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    
    if admin_id not in Owner:
        member = await chat.get_member(admin_id)
        if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            if not member.privileges.can_promote_members:
                return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ")
        else:
            return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        user_id, first_name, _ = await extract_user(client, message)

    if user_id is None:
        return await message.reply_text("User not found!")

    msg_text, result = await demote_user(user_id, first_name, admin_id, admin_name, chat_id, message)

    if not result:
        await message.reply_text(msg_text)

