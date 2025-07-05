from telethon import TelegramClient, events, Button
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import (
    ChatAdminRequiredError,
    UserAlreadyParticipantError,
    UserNotParticipantError,
    PhotoInvalidError,
)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantRequest
from pymongo import MongoClient
import asyncio
import os

from Bad.misc import SUDOERS
from Bad import Bad
from config import MONGO_DB_URI

# MongoDB setup
fsubdb = MongoClient(MONGO_DB_URI)
forcesub_collection = fsubdb.status_db.status

# Smallcap conversion dictionary (only used internally or for buttons)
SMALLCAPS = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ',
    'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
    'o': 'ᴏ', 'p': 'ᴘ', 'q': 'Q', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ',
    'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'
}

def to_smallcaps(text):
    return ''.join(SMALLCAPS.get(c.lower(), c) for c in text)

async def is_group_owner(event, chat_id, user_id):
    try:
        chat = await event.client.get_entity(chat_id)
        if hasattr(chat, 'creator') and chat.creator and chat.creator.id == user_id:
            return True
        return False
    except Exception:
        return False

@Bad.on(events.NewMessage(pattern=r'^/fsub\b'))
async def set_forcesub(event):
    chat_id = event.chat_id
    user_id = event.sender_id

    is_owner = await is_group_owner(event, chat_id, user_id)
    if user_id not in SUDOERS and not is_owner:
        await event.reply("**ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.**")
        return

    args = event.message.text.split(maxsplit=1)
    if len(args) < 2:
        await event.reply("**ᴜꜱᴀɢᴇ: /ғꜱᴜʙ <ᴄʜᴀɴɴᴇʟ ᴜꜱᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ> ᴏʀ /ғꜱᴜʙ ᴏꜰꜰ ᴛᴏ ᴅɪꜱᴀʙʟᴇ**")
        return

    command = args[1].lower()

    if command in ["off", "disable"]:
        forcesub_collection.delete_one({"chat_id": chat_id})
        await event.reply("**ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ ꜰᴏʀ ᴛʜɪꜱ ɢʀᴏᴜᴘ.**")
        return

    channel_input = command
    try:
        channel = await Bad.get_entity(channel_input)
        channel_id = channel.id
        channel_title = getattr(channel, 'title', 'Channel')
        if getattr(channel, 'username', None):
            channel_link = f"https://t.me/{channel.username}"
            channel_username = f"@{channel.username}"
        else:
            try:
                full_chat = await Bad(GetFullChannelRequest(channel))
                channel_link = full_chat.full_chat.exported_invite.link
            except Exception:
                channel_link = "https://t.me/"
            channel_username = channel_link

        bot_id = (await Bad.get_me()).id
        bot_is_admin = False
        async for admin in Bad.iter_participants(channel_id, filter=ChannelParticipantsAdmins):
            if admin.id == bot_id:
                bot_is_admin = True
                break

        if not bot_is_admin:
            await event.reply(
                message="**🚫 ɪ'ᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ᴄʜᴀɴɴᴇʟ.**\n\n**➲ ᴘʟᴇᴀꜱᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ:**\n\n**➥ ɪɴᴠɪᴛᴇ ɴᴇᴡ ᴍᴇᴍʙᴇʀꜱ**\n\n🛠️ **ᴛʜᴇɴ ᴜꜱᴇ /ғꜱᴜʙ <ᴄʜᴀɴɴᴇʟ ᴜꜱᴇʀɴᴀᴍᴇ> ᴛᴏ ꜱᴇᴛ ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.**",
                file="https://envs.sh/TnZ.jpg",
                buttons=[
                    [Button.url(to_smallcaps("๏ Add me in channel ๏"), f"https://t.me/{(await Bad.get_me()).username}?startchannel=s&admin=invite_users+manage_video_chats")]
                ]
            )
            return

        forcesub_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"channel_id": channel_id, "channel_username": channel_username}},
            upsert=True
        )

        set_by_user = (f"@{event.sender.username}" if getattr(event.sender, "username", None)
                      else (getattr(event.sender, "first_name", "User")))

        await event.reply(
            message=(
                f"**🎉 ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ꜱᴇᴛ ᴛᴏ** [{channel_title}]({channel_username}) **ꜰᴏʀ ᴛʜɪꜱ ɢʀᴏᴜᴘ.**\n\n"
                f"**🆔 ᴄʜᴀɴɴᴇʟ ɪᴅ:** `{channel_id}`\n"
                f"**🖇️ ᴄʜᴀɴɴᴇʟ ʟɪɴᴋ:** [ɢᴇᴛ ʟɪɴᴋ]({channel_link})\n"
                f"**👤 ꜱᴇᴛ ʙʏ:** {set_by_user}"
            ),
            file="https://envs.sh/Tn_.jpg",
            buttons=[[Button.inline(to_smallcaps("๏ Close ๏"), b"close_force_sub")]]
        )

    except Exception as e:
        await event.reply(
            message=(
                f"**❌ ᴇʀʀᴏʀ:** `{str(e)}`\n\n"
                "**➲ ᴘʟᴇᴀꜱᴇ ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ɪꜱ ᴘᴜʙʟɪᴄ ᴏʀ ᴛʜᴇ ʙᴏᴛ ɪꜱ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.**"
            ),
            file="https://envs.sh/TnZ.jpg",
            buttons=[
                [Button.url(to_smallcaps("๏ Add me in channel ๏"), f"https://t.me/{(await Bad.get_me()).username}?startchannel=s&admin=invite_users+manage_video_chats")]
            ]
        )

@Bad.on(events.CallbackQuery(pattern=b"close_force_sub"))
async def close_force_sub(event):
    await event.answer("ᴄʟᴏꜱᴇᴅ!")
    await event.delete()

async def check_forcesub(event):
    chat_id = event.chat_id
    user_id = event.sender_id

    forcesub_data = forcesub_collection.find_one({"chat_id": chat_id})
    if not forcesub_data:
        return True

    channel_id = forcesub_data["channel_id"]
    channel_username = forcesub_data["channel_username"]

    try:
        await Bad(GetParticipantRequest(channel_id, user_id))
        return True
    except UserNotParticipantError:
        await event.delete()
        channel_url = channel_username if channel_username.startswith("https://") else f"https://t.me/{channel_username.lstrip('@')}"

        try:
            user = await event.client.get_entity(user_id)
        except Exception:
            user = None

        sender_full_name = user.first_name if user else "User"
        if user and getattr(user, "last_name", None):
            sender_full_name += f" {user.last_name}"

        temp_file = f"profile_{user_id}.jpg"
        try:
            profile_pic_path = await event.client.download_profile_photo(user, temp_file)
        except Exception:
            profile_pic_path = None

        photo_arg = profile_pic_path if profile_pic_path and os.path.exists(profile_pic_path) else "https://envs.sh/TnZ.jpg"
        clickable_name = f"<a href='tg://user?id={user_id}'>{sender_full_name}</a>"

        await event.respond(
            message=(
                f"<b>👋 ʜᴇʟʟᴏ {clickable_name},</b>\n\n"
                f"<b>ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ <a href=\"{channel_url}\">ᴄʜᴀɴɴᴇʟ</a> ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ.</b>"
            ),
            file=photo_arg,
            buttons=[[Button.url(to_smallcaps("๏ Join Channel ๏"), channel_url)]],
            parse_mode='html'
        )
        if profile_pic_path and os.path.exists(profile_pic_path):
            try:
                os.remove(profile_pic_path)
            except Exception:
                pass

    except ChatAdminRequiredError:
        forcesub_collection.delete_one({"chat_id": chat_id})
        await event.respond("**🚫 ɪ'ᴍ ɴᴏ ʟᴏɴɢᴇʀ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ꜰᴏʀᴄᴇᴅ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴄʜᴀɴɴᴇʟ. ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ.**")
    return False

@Bad.on(events.NewMessage())
async def enforce_forcesub(event):
    if event.is_group and not event.sender.bot:
        if not await check_forcesub(event):
            raise events.StopPropagation

__MODULE__ = "ꜰᴏʀᴄᴇ ꜱᴜʙ"
__HELP__ = """
**<u>🔒 ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ</u>**

» `/fsub <channel_username>` – ᴇɴᴀʙʟᴇꜱ ꜰᴏʀᴄᴇꜱᴜʙ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀɴᴅ ʟɪɴᴋꜱ ɪᴛ ᴛᴏ ᴀ ᴄʜᴀɴɴᴇʟ.
» `/fsub off` – ᴅɪꜱᴀʙʟᴇ ꜰᴏʀᴄᴇ ꜱᴜʙ ꜰᴏʀ ᴛʜɪꜱ ɢʀᴏᴜᴘ.

• ᴏɴᴄᴇ ᴇɴᴀʙʟᴇᴅ, ᴜꜱᴇʀꜱ ᴡɪʟʟ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ʙᴇꜰᴏʀᴇ ᴛʜᴇʏ ᴄᴀɴ ᴍᴇꜱꜱᴀɢᴇ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.

**<u>⚙️ ʀᴇǫᴜɪʀᴇᴍᴇɴᴛꜱ</u>**
• ʙᴏᴛ ᴍᴜꜱᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.
• ᴀᴄᴄᴇꜱꜱ ᴛᴏ ɪɴᴠɪᴛᴇ ᴜꜱᴇʀꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ɪꜱ ᴍᴀɴᴅᴀᴛᴏʀʏ.

**<u>👤 ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ</u>**
• ᴄᴀɴ ʙᴇ ꜱᴇᴛ ʙʏ: **ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ** ᴏʀ **ꜱᴜᴅᴏ ᴜꜱᴇʀ**

**<u>💡 ɴᴏᴛᴇ:</u>**
• ᴛʜᴇ ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇꜱ ᴜꜱᴇʀ ᴍᴇꜱꜱᴀɢᴇꜱ ᴡʜᴏ ᴀʀᴇ ɴᴏᴛ ꜱᴜʙꜱᴄʀɪʙᴇᴅ.
• ɪᴛ ᴀʟꜱᴏ ɢɪᴠᴇꜱ ᴀ ʙᴜᴛᴛᴏɴ ꜰᴏʀ ᴜꜱᴇʀꜱ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.
"""
