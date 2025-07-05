import requests
import random
from Bad import app
from Bad.misc import SUDOERS
from pyrogram import *
from config import OWNER_ID
from pyrogram.types import *
from Bad.database.bad_bandb import admin_filter

bad_text = [
    "hey please don't disturb me.",
    "who are you",
    "aap kon ho",
    "aap mere owner to nhi lgte ",
    "hey tum mera name kyu le rhe ho meko sone do",
    "ha bolo kya kaam hai ",
    "dekho abhi mai busy hu ",
    "hey i am busy",
    "aapko smj nhi aata kya ",
    "leave me alone",
    "dude what happend",
]

strict_txt = [
    "i can't restrict against my besties",
    "are you serious i am not restrict to my friends",
    "fuck you bsdk k mai apne dosto ko kyu kru",
    "hey stupid admin ",
    "ha ye phele krlo maar lo ek dusre ki gwaand",
    "i can't hi is my closest friend",
    "i love him please don't restict this user try to usertand "
]

ban = ["ban", "boom"]
unban = ["unban",]
mute = ["mute", "silent", "shut"]
unmute = ["unmute", "speak", "free"]
kick = ["kick", "out", "nikaal", "nikal"]
promote = ["promote", "adminship", "admin"]
demote = ["demote", "lelo", "htado"]
fullpromote = ["fullpromote", "fullpower", "allparmishan", "allpower"]
group = ["group"]
channel = ["channel"]

# ========================================= #

@app.on_message(filters.command(["obo"], prefixes=["r", "R"]) & admin_filter)
async def restriction_app(app: app, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    if len(message.text) < 2:
        return await message.reply(random.choice(bad_text))
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")

    if reply:
        user_id = reply.from_user.id
        for banned in data:
            print(f"present {banned}")
            if banned in ban:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await message.reply("ᴏᴋ , ᴋᴀʀ ᴅɪᴀ ʙᴀɴ ᴍᴀᴅʀᴄʜᴏᴅ ᴋᴏ 😈 {message.from_user.first_name}")

        for unbanned in data:
            print(f"present {unbanned}")
            if unbanned in unban:
                await app.unban_chat_member(chat_id, user_id)
                await message.reply(f"ᴏᴋ , sɪʀ ᴋᴀʀ ᴅᴇᴛᴀ ʜᴜ ᴜɴʙᴀɴ 😏 {message.from_user.first_name}")

        for kicked in data:
            print(f"present {kicked}")
            if kicked in kick:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await app.unban_chat_member(chat_id, user_id)
                    await message.reply("ɢᴇᴛ ʟᴏsᴛ , ɴɪᴋʟ ᴍᴀᴅʀᴄʜᴏᴅ 🥱 {message.from_user.first_name}")

        for muted in data:
            print(f"present {muted}")
            if muted in mute:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    permissions = ChatPermissions(can_send_messages=False)
                    await message.chat.restrict_member(user_id, permissions)
                    await message.reply(f"ᴄʜᴜᴘ ᴋᴀʀ ʟᴏᴠᴅᴇ 😤 {message.from_user.first_name}")

        for unmuted in data:
            print(f"present {unmuted}")
            if unmuted in unmute:
                permissions = ChatPermissions(can_send_messages=True)
                await message.chat.restrict_member(user_id, permissions)
                await message.reply(f"ᴏʜ ! ᴏᴋᴀʏ sɪʀ ☺️ {message.from_user.first_name}")

        for promoted in data:
            print(f"present {promoted}")
            if promoted in promote:
                await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=False,
                    can_pin_messages=True,
                    can_promote_members=False,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                )
                )
                await message.reply("ᴀᴅᴍɪɴ ʙɴᴀ ᴅɪᴀ ʜᴀɪ ᴘʟᴢ ᴍᴇᴍʙᴇʀ ᴀᴅ ᴋᴀʀ ᴅᴇɴᴀ ᴛʜᴀɴᴋᴜ ❤️ {message.from_user.first_name}")

        for demoted in data:
            print(f"present {demoted}")
            if demoted in demote:
                await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False,
                )
                )
                await message.reply("ᴄʜᴜᴘ ᴋᴀʀ ᴋᴇ ʙᴇᴛʜᴀ ʀᴀʜ ʟᴏᴠᴅᴇ ᴀʙʜɪ ᴀᴅᴍɪɴ sᴇ ʜᴀᴛɪᴀ ʜᴀɪ ɪs ᴋᴇ ʙᴀᴀᴅ sɪᴅᴀ ɢʀᴏᴜᴘ ")

        for fullpromoted in data:
            print(f"present {fullpromoted}")
            if fullpromoted in fullpromote:
                await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                )
                )
                await message.reply("ғᴜʟʟ ᴀᴅᴍɪɴ ʙɴᴀ ᴅɪᴀ ʜᴀɪ ᴀʙʙ ᴀᴘɴᴇ ꜰʀɪᴇɴᴅ ᴋᴏ ʙɪ ᴀᴅᴅ ᴋᴀʀᴅᴏ ❤️ {message.from_user.first_name}")

@app.on_chat_member_updated()
async def promote_owner(client, chat_member_updated):
    if chat_member_updated.new_chat_member and chat_member_updated.new_chat_member.user:
        if chat_member_updated.new_chat_member.user.id == OWNER_ID:
            await client.promote_chat_member(
                chat_id=chat_member_updated.chat.id,
                user_id=OWNER_ID,
                privileges=ChatPrivileges(
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                )
            )
            await client.send_message(
                chat_id=chat_member_updated.chat.id,
                text="❤️"
)


__MODULE__ = "ʀᴇsᴛʀɪᴄᴛɪᴏɴ (ʀᴏʙᴏ)"
__HELP__ = """
**<u>ᴏʙᴏ ᴄᴏᴍᴍᴀɴᴅs 🧠</u>**

» `Robo ban` - ʙᴀɴ ᴀ ᴜꜱᴇʀ (ʀᴇᴘʟʏ).
» `Robo unban` - ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ (ʀᴇᴘʟʏ).
» `Robo mute` - ᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ (ʀᴇᴘʟʏ).
» `Robo unmute` - ᴜɴᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ (ʀᴇᴘʟʏ).
» `Robo kick` - ᴋɪᴄᴋ ᴀ ᴜꜱᴇʀ ꜰʀᴏᴍ ɢʀᴏᴜᴘ (ʀᴇᴘʟʏ).
» `Robo promote` - ɢɪᴠᴇ ʟɪᴍɪᴛᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.
» `Robo demote` - ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.
» `Robo fullpromote` - ꜰᴜʟʟ ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟᴇɢᴇꜱ.

**➥ All actions require replying to a user’s message.**
"""
