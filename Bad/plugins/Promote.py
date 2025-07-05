import random
import datetime
import requests
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid, BadRequest
from Bad import app, LOGGER
from Bad.misc import SUDOERS
from Bad.plugins.Ban import mention, extract_user
from config import LOG_GROUP_ID, OWNER_ID
from Pbx import Owner

async def promote_user(user_id, first_name, admin_id, admin_name, chat_id, message, time=None):
    try:
        user_status = await app.get_chat_member(chat_id, user_id)
        if user_status.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            msg_text = "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ."
            return msg_text, False

        await app.promote_chat_member(
            chat_id, 
            user_id, 
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=False,
                can_pin_messages=True,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=True
            )
        )
    except ChatAdminRequired:
        msg_text = "ɢɪᴠᴇ ᴍᴇ ᴘʀᴏᴍᴏᴛᴇ ʀɪɢʜᴛꜱ."
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "ɪ ᴡᴏɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴀɴ ᴀᴅᴍɪɴ."
        return msg_text, False
    except BadRequest as e:
        if "[400 USER_CREATOR]" in str(e):
            msg_text = "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ."
            return msg_text, False
        else:
            await message.reply_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ. ᴘʟᴇᴀꜱᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴀᴛ ᴛʜᴇ ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.\n\nᴇʀʀᴏʀ ᴛʏᴘᴇ: {e}")

    url = "https://api.waifu.pics/sfw/happy"
    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    
    button = [
        [InlineKeyboardButton(text="• ᴅᴇʟᴇᴛᴇ •", callback_data="close")]
    ]
    response = requests.get(url).json()
    pimg = response['url']
    
    await app.send_message(LOG_GROUP_ID, f"{user_mention} ᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ {admin_mention} ɪɴ {message.chat.title}")
    
    promoteee = await message.reply_video(
        video=pimg,
        caption=f"<u>ᴘʀᴏᴍᴏᴛᴇ ᴇᴠᴇɴᴛ</u>\n\nɴᴀᴍᴇ - {user_mention}\nᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ - {admin_mention}",
        reply_markup=InlineKeyboardMarkup(button)
    )

    return promoteee, True

@app.on_message(filters.command(["Promote"]))
async def promote(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    
    if admin_id not in Owner:
        member = await chat.get_member(admin_id)
        if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ.")
        if not member.privileges.can_promote_members:
            return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ.")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        user_id, first_name, _ = await extract_user(client, message)
        if not user_id:
            return await message.reply_text("ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ!")
    
    msg_text, result = await promote_user(user_id, first_name, admin_id, admin_name, chat_id, message)
    if not result:
        await message.reply_text(msg_text)

async def lowpromote_user(user_id, first_name, admin_id, admin_name, chat_id, message, time=None):
    try:
        user_status = await app.get_chat_member(chat_id, user_id)
        if user_status.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            msg_text = "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ."
            return msg_text, False

        await app.promote_chat_member(
            chat_id, 
            user_id, 
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=True,
                can_manage_video_chats=True
            )
        )
    except ChatAdminRequired:
        msg_text = "ɢɪᴠᴇ ᴍᴇ ᴘʀᴏᴍᴏᴛᴇ ʀɪɢʜᴛꜱ."
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "ɪ ᴡᴏɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴀɴ ᴀᴅᴍɪɴ."
        return msg_text, False
    except BadRequest as e:
        if "[400 USER_CREATOR]" in str(e):
            msg_text = "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ."
            return msg_text, False
        else:
            await message.reply_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ. ᴘʟᴇᴀꜱᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴀᴛ ᴛʜᴇ ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.\n\nᴇʀʀᴏʀ ᴛʏᴘᴇ: {e}")

    url = "https://api.waifu.pics/sfw/happy"
    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    
    button = [
        [InlineKeyboardButton(text="• ᴅᴇʟᴇᴛᴇ •", callback_data="close")]
    ]
    response = requests.get(url).json()
    pimg = response['url']
    
    await app.send_message(LOG_GROUP_ID, f"{user_mention} ʟᴏᴡ ᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ {admin_mention} ɪɴ {message.chat.title}")
    
    promoteee = await message.reply_video(
        video=pimg,
        caption=f"<u>ʟᴏᴡ ᴘʀᴏᴍᴏᴛᴇ ᴇᴠᴇɴᴛ</u>\n\nɴᴀᴍᴇ - {user_mention}\nᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ - {admin_mention}",
        reply_markup=InlineKeyboardMarkup(button)
    )

    return promoteee, True

@app.on_message(filters.command(["lowPromote"]))
async def lowpromote(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    
    if admin_id not in Owner:
        member = await chat.get_member(admin_id)
        if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ.")
        if not member.privileges.can_promote_members:
            return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ.")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        user_id, first_name, _ = await extract_user(client, message)
        if not user_id:
            return await message.reply_text("ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ!")
    
    msg_text, result = await lowpromote_user(user_id, first_name, admin_id, admin_name, chat_id, message)
    if not result:
        await message.reply_text(msg_text)

async def fullpromote_user(user_id, first_name, admin_id, admin_name, chat_id, message, time=None):
    try:
        user_status = await app.get_chat_member(chat_id, user_id)
        if user_status.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            msg_text = "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ."
            return msg_text, False

        await app.promote_chat_member(
            chat_id, 
            user_id, 
            privileges=ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True
            )
        )
    except ChatAdminRequired:
        msg_text = "ɢɪᴠᴇ ᴍᴇ ᴘʀᴏᴍᴏᴛᴇ ʀɪɢʜᴛꜱ."
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "ɪ ᴡᴏɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴀɴ ᴀᴅᴍɪɴ."
        return msg_text, False
    except BadRequest as e:
        if "[400 USER_CREATOR]" in str(e):
            msg_text = "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ."
            return msg_text, False
        else:
            await message.reply_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ. ᴘʟᴇᴀꜱᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴀᴛ ᴛʜᴇ ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.\n\nᴇʀʀᴏʀ ᴛʏᴘᴇ: {e}")

    url = "https://api.waifu.pics/sfw/happy"
    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    
    button = [
        [InlineKeyboardButton(text="• ᴅᴇʟᴇᴛᴇ •", callback_data="close")]
    ]
    response = requests.get(url).json()
    pimg = response['url']
    
    await app.send_message(LOG_GROUP_ID, f"{user_mention} ꜰᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ {admin_mention} ɪɴ {message.chat.title}")
    
    promoteee = await message.reply_video(
        video=pimg,
        caption=f"<u>ꜰᴜʟʟ ᴘʀᴏᴍᴏᴛᴇ ᴇᴠᴇɴᴛ</u>\n\nɴᴀᴍᴇ - {user_mention}\nᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ - {admin_mention}",
        reply_markup=InlineKeyboardMarkup(button)
    )

    return promoteee, True

@app.on_message(filters.command(["fullPromote"]))
async def fullpromote(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    
    if admin_id not in Owner:
        member = await chat.get_member(admin_id)
        if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ.")
        if not member.privileges.can_promote_members:
            return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ.")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        user_id, first_name, _ = await extract_user(client, message)
        if not user_id:
            return await message.reply_text("ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ!")
    
    msg_text, result = await fullpromote_user(user_id, first_name, admin_id, admin_name, chat_id, message)
    if not result:
        await message.reply_text(msg_text)


__MODULE__ = "ᴘʀᴏᴍᴏᴛᴇ"
__HELP__ = """ 

## ᴘʀᴏᴍᴏᴛᴇ 💢

» `/promote` [user_id / username / reply] : ᴘʀᴏᴍᴏᴛᴇ ᴜꜱᴇʀ ᴡɪᴛʜ ɴᴏʀᴍᴀʟ ʀɪɢʜᴛꜱ  
» `/lowpromote` [user_id / username / reply] : ᴘʀᴏᴍᴏᴛᴇ ᴜꜱᴇʀ ᴡɪᴛʜ ʟᴏᴡ ʀɪɢʜᴛꜱ  
» `/fullpromote` [user_id / username / reply] : ᴘʀᴏᴍᴏᴛᴇ ᴜꜱᴇʀ ᴡɪᴛʜ ꜰᴜʟʟ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ  
» `/demote` [user_id / username / reply] : ʀᴇᴍᴏᴠᴇ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴀᴅᴍɪɴꜱ

"""
