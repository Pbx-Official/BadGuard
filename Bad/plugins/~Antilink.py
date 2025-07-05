from pyrogram import Client, filters
from pyrogram.types import Message
import re
from collections import defaultdict

# Regex for link detection
LINK_REGEX = r"(https?://\S+|www\.\S+|\S+\.(com|in|net|org|info|xyz))"

# User spam tracking
user_message_times = defaultdict(list)

# Filter states
anti_link_enabled = defaultdict(lambda: False)
anti_file_enabled = defaultdict(lambda: False)

# Command to enable/disable anti-link and anti-file
@app.on_message(filters.command(["antifilter", "antifilter@YourBotUsername"]) & filters.group)
async def toggle_filters(client: Client, message: Message):
    if not message.from_user:
        return

    # Check if user is admin
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_member = await client.get_chat_member(chat_id, user_id)
    
    if chat_member.status not in ["administrator", "creator"]:
        await message.reply_text("Only admins can use this command!")
        return

    command_parts = message.text.split()
    if len(command_parts) < 3:
        await message.reply_text(
            "Usage: /antifilter [link|file] [enable|disable]\n"
            "Example: /antifilter link enable"
        )
        return

    filter_type = command_parts[1].lower()
    action = command_parts[2].lower()

    if filter_type not in ["link", "file"]:
        await message.reply_text("Invalid filter type! Use 'link' or 'file'.")
        return

    if action not in ["enable", "disable"]:
        await message.reply_text("Invalid action! Use 'enable' or 'disable'.")
        return

    if filter_type == "link":
        anti_link_enabled[chat_id] = (action == "enable")
        status = "enabled" if action == "enable" else "disabled"
        await message.reply_text(f"Anti-link filter has been {status}.")
    elif filter_type == "file":
        anti_file_enabled[chat_id] = (action == "enable")
        status = "enabled" if action == "enable" else "disabled"
        await message.reply_text(f"Anti-file filter has been {status}.")

# Anti-Link Filter
@app.on_message(filters.group & filters.text & ~filters.private)
async def anti_link(_, message: Message):
    if not anti_link_enabled[message.chat.id]:
        return

    if re.search(LINK_REGEX, message.text.lower()):
        try:
            if message.from_user:  # Check if message has a sender
                await message.delete()
                warning = f"{message.from_user.mention} ʟɪɴᴋꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."
                await message.reply_text(warning)
        except Exception as e:
            print(f"Link Deletion Error: {e}")

# Anti-File Filter
@app.on_message(filters.group & filters.document)
async def anti_files(_, message: Message):
    if not anti_file_enabled[message.chat.id]:
        return

    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.mp3', '.mp4')
    
    try:
        if not message.document or not message.document.file_name:
            return

        file_name = message.document.file_name.lower()
        if not file_name.endswith(allowed_extensions):
            await message.delete()
            if message.from_user:  # Check if message has a sender
                warning = f"{message.from_user.mention} ꜰɪʟᴇꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."
                await message.reply_text(warning)
    except Exception as e:
        print(f"File Deletion Error: {e}")
