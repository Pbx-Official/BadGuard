import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from Bad import app
from Bad.misc import SUDOERS
from Bad.database import get_readable_time
from Bad.database.database import (
    add_banned_user,
    get_banned_count,
    get_banned_users,
    get_served_chats,
    is_banned_user,
    remove_banned_user,
)
from Bad.database.extractiondb import extract_user
from config import BANNED_USERS

# Translation dictionary
_ = {
    "general_1": "❖ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ.",
    "gban_1": "❖ ᴡʜʏ ᴅɪᴅ ʏᴏᴜ ᴡᴀɴɴᴀ ɢʙᴀɴ ʏᴏᴜʀsᴇʟғ ʙᴀʙʏ ?",
    "gban_2": "❖ ᴡʜʏ sʜᴏᴜʟᴅ ɪ ɢʙᴀɴ ᴍʏsᴇʟғ ?",
    "gban_3": "❖ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ᴍʏ sᴜᴅᴏᴇʀs.",
    "gban_4": "❖ {0} ɪs ᴀʟʀᴇᴀᴅʏ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.",
    "gban_5": "❖ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ {0}.\n\n<b>● ᴛɪᴍᴇ ᴇxᴘᴇᴄᴛᴇᴅ ➥</b> {1}",
    "gban_6": "<b>❖ ɴᴇᴡ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ {0} ➥</b>\n\n<b>● ᴏʀɪɢɪɴᴀᴛᴇᴅ ғʀᴏᴍ ➥</b> {1} [<code>{2}</code>]\n<b>● ᴜsᴇʀ :➥</b> {3}\n<b>● ᴜsᴇʀ ɪᴅ ➥</b> {4}\n\n<b>● ʙᴀɴɴᴇᴅ ʙʏ ➥</b> {5}\n<b>● ᴄʜᴀᴛs ➥</b> </code>{6}</code>",
    "gban_7": "❖ {0} ɪs ɴᴏᴛ ɢʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.",
    "gban_8": "❖ ʟɪғᴛɪɴɢ ɢʟᴏʙᴀʟ ʙᴀɴ ғʀᴏᴍ {0}.\n\n<b>● ᴇxᴘᴇᴄᴛᴇᴅ ᴛɪᴍᴇ ➥</b> {1}",
    "gban_9": "❖ ʟɪғᴛᴇᴅ ɢʟᴏʙᴀʟ ʙᴀɴ ғʀᴏᴍ {0}.\n\n● ᴜɴʙᴀɴɴᴇᴅ ɪɴ {1} ᴄʜᴀᴛs.",
    "gban_10": "❖ ɴᴏ ᴏɴᴇ ɪs ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.",
    "gban_11": "❖ ғᴇᴛᴄʜɪɴɢ ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs ʟɪsᴛ...",
    "gban_12": "❖ <b>ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ➥</b>\n\n"
}

@app.on_message(filters.command(["gban", "globalban"]) & SUDOERS)
async def global_ban(client, message: Message):
    try:
        # Check if it's a reply or command with user identifier
        if message.reply_to_message:
            user = await extract_user(message.reply_to_message)
        else:
            if len(message.command) < 2:
                return await message.reply_text(_["general_1"])
            user = await extract_user(message)
        
        if not user:
            return await message.reply_text(_["general_1"])
            
        if user.id == message.from_user.id:
            return await message.reply_text(_["gban_1"])
        elif user.id == app.id:
            return await message.reply_text(_["gban_2"])
        elif user.id in SUDOERS:
            return await message.reply_text(_["gban_3"])
            
        is_gbanned = await is_banned_user(user.id)
        if is_gbanned:
            return await message.reply_text(_["gban_4"].format(user.mention))
            
        if user.id not in BANNED_USERS:
            BANNED_USERS.add(user.id)
            
        served_chats = []
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
            
        time_expected = get_readable_time(len(served_chats))
        mystic = await message.reply_text(_["gban_5"].format(user.mention, time_expected))
        number_of_chats = 0
        
        for chat_id in served_chats:
            try:
                await app.ban_chat_member(chat_id, user.id)
                number_of_chats += 1
            except FloodWait as fw:
                await asyncio.sleep(int(fw.value))
            except:
                continue
                
        await add_banned_user(user.id)
        await message.reply_text(
            _["gban_6"].format(
                app.mention,
                message.chat.title,
                message.chat.id,
                user.mention,
                user.id,
                message.from_user.mention,
                number_of_chats,
            )
        )
        await mystic.delete()
        
    except Exception as e:
        await message.reply_text(_["general_2"].format(str(e)))

@app.on_message(filters.command(["ungban"]) & SUDOERS)
async def global_un(client, message: Message):
    try:
        # Check if it's a reply or command with user identifier
        if message.reply_to_message:
            user = await extract_user(message.reply_to_message)
        else:
            if len(message.command) < 2:
                return await message.reply_text(_["general_1"])
            user = await extract_user(message)
            
        if not user:
            return await message.reply_text(_["general_1"])
            
        is_gbanned = await is_banned_user(user.id)
        if not is_gbanned:
            return await message.reply_text(_["gban_7"].format(user.mention))
            
        if user.id in BANNED_USERS:
            BANNED_USERS.remove(user.id)
            
        served_chats = []
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
            
        time_expected = get_readable_time(len(served_chats))
        mystic = await message.reply_text(_["gban_8"].format(user.mention, time_expected))
        number_of_chats = 0
        
        for chat_id in served_chats:
            try:
                await app.unban_chat_member(chat_id, user.id)
                number_of_chats += 1
            except FloodWait as fw:
                await asyncio.sleep(int(fw.value))
            except:
                continue
                
        await remove_banned_user(user.id)
        await message.reply_text(_["gban_9"].format(user.mention, number_of_chats))
        await mystic.delete()
        
    except Exception as e:
        await message.reply_text(_["general_2"].format(str(e)))

@app.on_message(filters.command(["gbannedusers", "gbanlist"]) & SUDOERS)
async def gbanned_list(client, message: Message):
    try:
        counts = await get_banned_count()
        if counts == 0:
            return await message.reply_text(_["gban_10"])
            
        mystic = await message.reply_text(_["gban_11"])
        msg = _["gban_12"]
        count = 0
        users = await get_banned_users()
        
        for user_id in users:
            count += 1
            try:
                user = await app.get_users(user_id)
                user_name = user.first_name if not user.mention else user.mention
                msg += f"{count}➤ {user_name}\n"
            except Exception:
                msg += f"{count}➤ {user_id}\n"
                continue
                
        if count == 0:
            await mystic.edit_text(_["gban_10"])
        else:
            await mystic.edit_text(msg)
            
    except Exception as e:
        await message.reply_text(_["general_2"].format(str(e)))