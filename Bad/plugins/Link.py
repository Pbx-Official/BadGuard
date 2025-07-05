import os

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from Bad import app
from Bad.misc import SUDOERS


# Command handler for /givelink command
@app.on_message(filters.command("givelink"))
async def give_link_command(client, message):
    # Generate an invite link for the chat where the command is used
    chat = message.chat.id
    link = await app.export_chat_invite_link(chat)
    await message.reply_text(f"Here's the invite link for this chat:\n{link}")


@app.on_message(
    filters.command(
        ["link", "invitelink"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]
    )
    & SUDOERS
)
async def link_command_handler(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("Invalid usage. Correct format: /link group_id")
        return

    group_id = message.command[1]
    file_name = f"group_info_{group_id}.txt"

    try:
        chat = await client.get_chat(int(group_id))

        if chat is None:
            await message.reply("Unable to get information for the specified group ID.")
            return

        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except FloodWait as e:
            await message.reply(f"FloodWait: {e.x} seconds. Retrying in {e.x} seconds.")
            return

        group_data = {
            "id": chat.id,
            "type": str(chat.type),
            "title": chat.title,
            "members_count": chat.members_count,
            "description": chat.description,
            "invite_link": invite_link,
            "is_verified": chat.is_verified,
            "is_restricted": chat.is_restricted,
            "is_creator": chat.is_creator,
            "is_scam": chat.is_scam,
            "is_fake": chat.is_fake,
            "dc_id": chat.dc_id,
            "has_protected_content": chat.has_protected_content,
        }

        with open(file_name, "w", encoding="utf-8") as file:
            for key, value in group_data.items():
                file.write(f"{key}: {value}\n")

        await client.send_document(
            chat_id=message.chat.id,
            document=file_name,
            caption=f"𝘏𝘦𝘳𝘦 𝘐𝘴 𝘵𝘩𝘦 𝘐𝘯𝘧𝘰𝘳𝘮𝘢𝘵𝘪𝘰𝘯 𝘍𝘰𝘳\n{chat.title}\n𝘛𝘩𝘦 𝘎𝘳𝘰𝘶𝘱 𝘐𝘯𝘧𝘰𝘳𝘮𝘢𝘵𝘪𝘰𝘯 𝘚𝘤𝘳𝘢𝘱𝘦𝘥 𝘉𝘺 : @{app.username}",
        )

    except Exception as e:
        await message.reply(f"Error: {str(e)}")

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

__MODULE__ = "ɢᴄ ʟɪɴᴋ"
__HELP__ = """
**<u>🔗 ɢʀᴏᴜᴘ ɪɴᴠɪᴛᴇ ʟɪɴᴋ</u>**

» `/givelink` – ɢᴇᴛ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ꜰᴏʀ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ɢʀᴏᴜᴘ.

**<u>📂 ɢʀᴏᴜᴘ ɪɴꜰᴏ ꜰᴇᴛᴄʜᴇʀ</u>** [**sᴜᴅᴏ ᴏɴʟʏ**]

» `/link <group_id>` – ꜰᴇᴛᴄʜ ɢʀᴏᴜᴘ ɪɴꜰᴏ ᴀɴᴅ sᴀᴠᴇ ɪᴛ ɪɴ ᴀ ᴛᴇxᴛ ꜰɪʟᴇ:
   • ID
   • Title
   • Type
   • Member count
   • Description
   • Invite link
   • Verified, Scam, Fake status
   • Data center ID (dc_id)
   • Protected content status

⏎ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʀᴇᴘʟɪᴇs ᴡɪᴛʜ ᴀ .txt ꜰɪʟᴇ ᴄᴏɴᴛᴀɪɴɪɴɢ ᴅᴇᴛᴀɪʟs.
"""
