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
        return await message.reply_text("🚫 Only admins can toggle anti-link.")
    
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/antilink on` or `/antilink off`")

    arg = message.command[1].lower()
    if arg == "on":
        anti_link_enabled[message.chat.id] = True
        await message.reply_text("✅ Anti-Link has been **enabled**.")
    elif arg == "off":
        anti_link_enabled[message.chat.id] = False
        await message.reply_text("❌ Anti-Link has been **disabled**.")
    else:
        await message.reply_text("Usage: `/antilink on` or `/antilink off`")

# Anti-Link Filter
@app.on_message(filters.group & filters.text & ~filters.private)
async def anti_link_filter(_, message: Message):
    if not anti_link_enabled[message.chat.id]:
        return

    if re.search(LINK_REGEX, message.text.lower()):
        try:
            await message.delete()
            warning = f"{message.from_user.mention} ⚠️ ʟɪɴᴋꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."
            await message.reply_text(warning)
        except Exception as e:
            print("Link Deletion Error:", e)

# Enable/Disable Anti-File
@app.on_message(filters.command("antifile", prefixes="/") & filters.group)
async def toggle_anti_file(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text("🚫 Only admins can toggle anti-file.")
    
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/antifile on` or `/antifile off`")

    arg = message.command[1].lower()
    if arg == "on":
        anti_file_enabled[message.chat.id] = True
        await message.reply_text("✅ Anti-File has been **enabled**.")
    elif arg == "off":
        anti_file_enabled[message.chat.id] = False
        await message.reply_text("❌ Anti-File has been **disabled**.")
    else:
        await message.reply_text("Usage: `/antifile on` or `/antifile off`")

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
            warning = f"{message.from_user.mention} ⚠️ ꜰɪʟᴇꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."
            await message.reply_text(warning)
    except Exception as e:
        print("File Deletion Error:", e)