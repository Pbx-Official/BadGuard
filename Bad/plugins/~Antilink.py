from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from Bad import app
import re
from collections import defaultdict

# Regex for detecting links
LINK_REGEX = r"(https?://\S+|www\.\S+|\S+\.(com|in|net|org|info|xyz))"

# Group-wise toggle states
anti_link_enabled = defaultdict(lambda: False)
anti_file_enabled = defaultdict(lambda: False)

# Smallcaps mapping
SMALLCAPS = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ',
    'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
    'o': 'ᴏ', 'p': 'ᴘ', 'q': 'Q', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ',
    'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'
}

def to_smallcaps(text: str) -> str:
    return ''.join(SMALLCAPS.get(c.lower(), c) for c in text)

async def is_admin(client, message: Message) -> bool:
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
    except:
        return False

# --- Commands ---

@app.on_message(filters.command("antilink") & filters.group)
async def toggle_anti_link(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text(to_smallcaps("🚫 ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴛᴏɢɢʟᴇ ᴀɴᴛɪ-ʟɪɴᴋ."))
    
    if len(message.command) < 2:
        return await message.reply_text(to_smallcaps("ᴜꜱᴀɢᴇ: `/antilink on` ᴏʀ `/antilink off`"))

    arg = message.command[1].lower()
    anti_link_enabled[message.chat.id] = arg == "on"
    status = "ᴇɴᴀʙʟᴇᴅ" if arg == "on" else "ᴅɪꜱᴀʙʟᴇᴅ"
    symbol = "✅" if arg == "on" else "❌"
    await message.reply_text(to_smallcaps(f"{symbol} ᴀɴᴛɪ-ʟɪɴᴋ ʜᴀꜱ ʙᴇᴇɴ **{status}**."))

@app.on_message(filters.command("antifile") & filters.group)
async def toggle_anti_file(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text(to_smallcaps("🚫 ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴛᴏɢɢʟᴇ ᴀɴᴛɪ-ꜰɪʟᴇ."))
    
    if len(message.command) < 2:
        return await message.reply_text(to_smallcaps("ᴜꜱᴀɢᴇ: `/antifile on` ᴏʀ `/antifile off`"))

    arg = message.command[1].lower()
    anti_file_enabled[message.chat.id] = arg == "on"
    status = "ᴇɴᴀʙʟᴇᴅ" if arg == "on" else "ᴅɪꜱᴀʙʟᴇᴅ"
    symbol = "✅" if arg == "on" else "❌"
    await message.reply_text(to_smallcaps(f"{symbol} ᴀɴᴛɪ-ꜰɪʟᴇ ʜᴀꜱ ʙᴇᴇɴ **{status}**."))

# --- Filters ---

@app.on_message(filters.group & filters.text & ~filters.private)
async def anti_link_filter(_, message: Message):
    if not anti_link_enabled[message.chat.id]:
        return
    if re.search(LINK_REGEX, message.text.lower()):
        try:
            await message.delete()
            await message.reply_text(to_smallcaps(f"{message.from_user.mention} ⚠️ ʟɪɴᴋꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."))
        except Exception as e:
            print(f"[AntiLink] Error: {e}")

@app.on_message(filters.group & filters.document)
async def anti_file_filter(_, message: Message):
    if not anti_file_enabled[message.chat.id]:
        return
    allowed_exts = ('.jpg', '.jpeg', '.png', '.gif', '.mp3', '.mp4')
    try:
        if message.document and not message.document.file_name.lower().endswith(allowed_exts):
            await message.delete()
            await message.reply_text(to_smallcaps(f"{message.from_user.mention} ⚠️ ꜰɪʟᴇꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."))
    except Exception as e:
        print(f"[AntiFile] Error: {e}")
