from pyrogram import filters
from pyrogram.types import Message

from Bad import app
from Bad.misc import SUDOERS
from Bad.database.database import add_gban_user, remove_gban_user
from Bad.database.extractiondb import extract_user
from config import BANNED_USERS

# Translation dictionary
_ = {
    "general_1": "❖ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ.",
    "block_1": "❖ {0} ɪs ᴀʟʀᴇᴀᴅʏ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.",
    "block_2": "❖ ᴀᴅᴅᴇᴅ {0} ᴛᴏ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ʟɪsᴛ.",
    "block_3": "❖ {0} ɪs ɴᴏᴛ ɪɴ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ʟɪsᴛ.",
    "block_4": "❖ ʀᴇᴍᴏᴠᴇᴅ {0} ғʀᴏᴍ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ʟɪsᴛ.",
    "block_5": "❖ ɴᴏ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ғᴏᴜɴᴅ.",
    "block_6": "❖ ɢᴇᴛᴛɪɴɢ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ʟɪsᴛ...",
    "block_7": "❖ <b>ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ➥</b>\n\n"
}

@app.on_message(filters.command(["block"]) & SUDOERS)
async def useradd(client, message: Message):
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
            
        if user.id in BANNED_USERS:
            return await message.reply_text(_["block_1"].format(user.mention))
            
        await add_gban_user(user.id)
        BANNED_USERS.add(user.id)
        await message.reply_text(_["block_2"].format(user.mention))
        
    except Exception as e:
        await message.reply_text(_["general_2"].format(str(e)))

@app.on_message(filters.command(["unblock"]) & SUDOERS)
async def userdel(client, message: Message):
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
            
        if user.id not in BANNED_USERS:
            return await message.reply_text(_["block_3"].format(user.mention))
            
        await remove_gban_user(user.id)
        BANNED_USERS.remove(user.id)
        await message.reply_text(_["block_4"].format(user.mention))
        
    except Exception as e:
        await message.reply_text(_["general_2"].format(str(e)))

@app.on_message(filters.command(["blocked", "blockedusers", "blusers"]) & SUDOERS)
async def sudoers_list(client, message: Message):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
        
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    
    for user_id in BANNED_USERS:
        try:
            user = await app.get_users(user_id)
            user_name = user.first_name if not user.mention else user.mention
            count += 1
            msg += f"{count}➤ {user_name}\n"
        except Exception:
            continue
            
        if count == 0:
            return await mystic.edit_text(_["block_5"])
        return await mystic.edit_text(msg)
        
    except Exception as e:
        await message.reply_text(_["general_2"].format(str(e)))