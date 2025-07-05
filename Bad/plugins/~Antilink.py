from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from Bad import app  # Replace with your Client if needed
import re
from collections import defaultdict

# Regex for link detection
LINK_REGEX = r"(https?://\S+|www\.\S+|\S+\.(com|in|net|org|info|xyz))"

# Group-wise settings
anti_link_enabled = defaultdict(lambda: False)
anti_file_enabled = defaultdict(lambda: False)

# Smallcap conversion dictionary
SMALLCAPS = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ',
    'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
    'o': 'ᴏ', 'p': 'ᴘ', 'q': 'Q', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ',
    'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'
}

def to_smallcaps(text):
    return ''.join(SMALLCAPS.get(c.lower(), c) for c in text)

# Admin check
async def is_admin(client, message: Message) -> bool:
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
    except:
        return False

# Enable/Disable Anti-Link
@app.on_message(filters.command("antilink", prefixes="/") & filters.group)
async def toggle_anti_link(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text(to_smallcaps("🚫 ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴛᴏɢɢʟᴇ ᴀɴᴛɪ-ʟɪɴᴋ."))
    
    if len(message.command) < 2:
        return await message.reply_text(to_smallcaps("ᴜꜱᴀɢᴇ: `/antilink on` ᴏʀ `/antilink off`"))

    arg = message.command[1].lower()
    if arg == "on":
        anti_link_enabled[message.chat.id] = True
        await message.reply_text(to_smallcaps("✅ ᴀɴᴛɪ-ʟɪɴᴋ ʜᴀꜱ ʙᴇᴇɴ **ᴇɴᴀʙʟᴇᴅ**."))
    elif arg == "off":
        anti_link_enabled[message.chat.id] = False
        await message.reply_text(to_smallcaps("❌ ᴀɴᴛɪ-ʟɪɴᴋ ʜᴀꜱ ʙᴇᴇɴ **ᴅɪꜱᴀʙʟᴇᴅ**."))
    else:
        await message.reply_text(to_smallcaps("ᴜꜱᴀɢᴇ: `/antilink on` ᴏʀ `/antilink off`"))

# Anti-Link Filter
@app.on_message(filters.group & filters.text & ~filters.private)
async def anti_link_filter(_, message: Message):
    if not anti_link_enabled[message.chat.id]:
        return

    if re.search(LINK_REGEX, message.text.lower()):
        try:
            await message.delete()
            warning = to_smallcaps(f"{message.from_user.mention} ⚠️ ʟɪɴᴋꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ.")
            await message.reply_text(warning)
        except Exception as e:
            print(f"Link Deletion Error in chat {message.chat.id}: {e}")

# Enable/Disable Anti-File
@app.on_message(filters.command("antifile", prefixes="/") & filters.group)
async def toggle_anti_file(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text(to_smallcaps("🚫 ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴛᴏɢɢʟᴇ ᴀɴᴛɪ-ꜰɪʟᴇ."))
    
    if len(message.command) < 2:
        return await message.reply_text(to_smallcaps("ᴜꜱᴀɢᴇ: `/antifile on` ᴏʀ `/antifile off`"))

    arg = message.command[1].lower()
    if arg == "on":
        anti_file_enabled[message.chat.id] = True
        await message.reply_text(to_smallcaps("✅ ᴀɴᴛɪ-ꜰɪʟᴇ ʜᴀꜱ ʙᴇᴇɴ **ᴇɴᴀʙʟᴇᴅ**."))
    elif arg == "off":
        anti_file_enabled[message.chat.id] = False
        await message.reply_text(to_smallcaps("❌ ᴀɴᴛɪ-ꜰɪʟᴇ ʜᴀꜱ ʙᴇᴇɴ **ᴅɪꜱᴀʙʟᴇᴅ**."))
    else:
        await message.reply_text(to_smallcaps("ᴜꜱᴀɢᴇ: `/antifile on` ᴏʀ `/antifile off`"))

# Anti-File Filter
@app.on_message(filters.group & filters.document)
async def anti_file_filter(_, message: Message):
    if not anti_file_enabled[message.chat.id]:
        return

    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.mp3', '.mp4')
    try:
        file_name = message.document.file_name.lower()
        if not file_name.endswith(allowed_extensions):
            await message.delete()
            warning = to_smallcaps(f"{message.from_user.mention} ⚠️ ꜰɪʟᴇꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ.")
            await message.reply_text(warning)
    except Exception as e:
        print(f"File Deletion Error in chat {message.chat.id}: {e}")

__MODULE__ = to_smallcaps("ᴀɴᴛɪ ʟɪɴᴋ")
__HELP__ = """
**<u>ᴀɴᴛɪ-ʟɪɴᴋ 🚫</u>**
» `/antilink on` - ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇꜱ ᴄᴏɴᴛᴀɪɴɪɴɢ ʟɪɴᴋꜱ.
» `/antilink off` - ᴅɪꜱᴀʙʟᴇ ᴀɴᴛɪ-ʟɪɴᴋ ꜰɪʟᴛᴇʀ.

**<u>ᴀɴᴛɪ-ꜰɪʟᴇ 📂</u>**
» `/antifile on` - ʙʟᴏᴄᴋ ᴀʟʟ ᴜɴᴡᴀɴᴛᴇᴅ ꜰɪʟᴇꜱ (ᴇxᴄᴇᴘᴛ ɪᴍᴀɢᴇꜱ, ᴠɪᴅᴇᴏꜱ, ᴀᴜᴅɪᴏ).
» `/antifile off` - ᴀʟʟᴏᴡ ᴀʟʟ ꜰɪʟᴇ ᴛʏᴘᴇꜱ.

**⛔️ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜᴇꜱᴇ ᴄᴏᴍᴍᴀɴᴅꜱ.**

➥ ᴀʟʟ ᴠɪᴏʟᴀᴛɪᴏɴꜱ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʀᴇꜱᴜʟᴛ ɪɴ ᴍᴇꜱꜱᴀɢᴇ ᴅᴇʟᴇᴛɪᴏɴ + ᴡᴀʀɴɪɴɢ.
"""
