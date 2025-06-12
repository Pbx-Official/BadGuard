from pyrogram import filters
from pyrogram.types import Message

from Bad import app
from Bad.misc import SUDOERS
from Bad.database.database import add_sudo, remove_sudo
from Bad.database.extractiondb import extract_user
from Bad.database.Buttons import close_markup
from config import BANNED_USERS, OWNER_ID

# Message strings dictionary
_ = {
    "general_1": "❖ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ.",
    "sudo_1": "❖ {0} ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.",
    "sudo_2": "❖ ᴀᴅᴅᴇᴅ {0} ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.",
    "sudo_3": "❖ {0} ɪs ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.",
    "sudo_4": "❖ ʀᴇᴍᴏᴠᴇᴅ {0} ғʀᴏᴍ sᴜᴅᴏ ᴜsᴇʀs ʟɪsᴛ.",
    "sudo_5": "<b>❖ ᴏᴡɴᴇʀ ➥</b>\n",
    "sudo_6": "\n❖ <b>sᴜᴅᴏ ᴜsᴇʀs ➥</b>\n",
    "sudo_7": "❖ ɴᴏ sᴜᴅᴏ ᴜsᴇʀs ғᴏᴜɴᴅ.",
    "sudo_8": "❖ ғᴀɪʟᴇᴅ."
}

@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
async def useradd(client, message: Message):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if not user:
        return await message.reply_text(_["general_1"])
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])

@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
async def userdel(client, message: Message):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if not user:
        return await message.reply_text(_["general_1"])
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])

@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & ~BANNED_USERS)
async def sudoers_list(client, message: Message):
    text = _["sudo_5"]
    try:
        user = await app.get_users(OWNER_ID)
        user_mention = user.mention if user.mention else user.first_name
        text += f"1➤ {user_mention}\n"
    except:
        text += "1➤ Owner (ID: {0})\n".format(OWNER_ID)
    
    count = 1
    smex = 0
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user_mention = user.mention if user.mention else user.first_name
                if smex == 0:
                    smex += 1
                    text += _["sudo_6"]
                count += 1
                text += f"{count}➤ {user_mention}\n"
            except:
                continue
    
    if count == 1:
        await message.reply_text(_["sudo_7"])
    else:
        await message.reply_text(text, reply_markup=close_markup())