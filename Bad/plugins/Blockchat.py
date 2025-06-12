from pyrogram import filters
from pyrogram.types import Message

from Bad import app
from Bad.misc import SUDOERS
from Bad.database.database import blacklist_chat, blacklisted_chats, whitelist_chat
from config import BANNED_USERS

# Translation dictionary
_ = {
    "black_1": "❖ <b>ᴇxᴀᴍᴘʟᴇ ➥</b>\n\n● /blacklistchat [ᴄʜᴀᴛ ɪᴅ]",
    "black_2": "❖ ᴛʜɪs ᴄʜᴀᴛ ɪs ᴀʟʀᴇᴀᴅʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ.",
    "black_3": "❖ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs.",
    "black_4": "❖ <b>ᴇxᴀᴍᴘʟᴇ ➥</b>\n\n● /whitelistchat [ᴄʜᴀᴛ ɪᴅ]",
    "black_5": "❖ ᴛʜɪs ᴄʜᴀᴛ ɪs ɴᴏᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ.",
    "black_6": "❖ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs.",
    "black_7": "❖ ʟɪsᴛ ᴏғ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs ➥\n\n",
    "black_8": "❖ ɴᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs ᴏɴ {0}.",
    "black_9": "❖ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ."
}

@app.on_message(filters.command(["blchat", "blacklistchat"]) & SUDOERS)
async def blacklist_chat_func(client, message: Message, _):
    try:
        if len(message.command) != 2:
            return await message.reply_text(_["black_1"])
        chat_id = int(message.text.strip().split()[1])
        if chat_id in await blacklisted_chats():
            return await message.reply_text(_["black_2"])
        blacklisted = await blacklist_chat(chat_id)
        if blacklisted:
            await message.reply_text(_["black_3"])
        else:
            await message.reply_text(_["black_9"])
        try:
            await app.leave_chat(chat_id)
        except:
            pass
    except Exception as e:
        await message.reply_text(_["black_9"])

@app.on_message(filters.command(["whitelistchat", "unblacklistchat", "unblchat"]) & SUDOERS)
async def white_funciton(client, message: Message, _):
    try:
        if len(message.command) != 2:
            return await message.reply_text(_["black_4"])
        chat_id = int(message.text.strip().split()[1])
        if chat_id not in await blacklisted_chats():
            return await message.reply_text(_["black_5"])
        whitelisted = await whitelist_chat(chat_id)
        if whitelisted:
            await message.reply_text(_["black_6"])
        else:
            await message.reply_text(_["black_9"])
    except Exception as e:
        await message.reply_text(_["black_9"])

@app.on_message(filters.command(["blchats", "blacklistedchats"]) & ~BANNED_USERS)
async def all_chats(client, message: Message, _):
    try:
        text = _["black_7"]
        j = 0
        for count, chat_id in enumerate(await blacklisted_chats(), 1):
            try:
                title = (await app.get_chat(chat_id)).title
            except:
                title = "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
            j = 1
            text += f"{count}. {title}[<code>{chat_id}</code>]\n"
        if j == 0:
            await message.reply_text(_["black_8"].format(app.mention))
        else:
            await message.reply_text(text)
    except Exception as e:
        await message.reply_text(_["black_9"])
