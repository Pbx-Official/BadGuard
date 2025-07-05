from pyrogram import filters

from Bad import app


@app.on_message(filters.command("id"))
async def get_id(client, message):
    try:
        if message.reply_to_message:
            if message.reply_to_message.sticker:

                if message.reply_to_message.forward_from_chat:
                    await message.reply(
                        f"The forwarded {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} has an ID of <code>{message.reply_to_message.forward_from_chat.id}</code>."
                    )
                elif message.reply_to_message.forward_from:
                    await message.reply(
                        f"The forwarded user, {message.reply_to_message.forward_from.first_name} has an ID of <code>{message.reply_to_message.forward_from.id}</code>."
                    )
                elif message.reply_to_message.forward_sender_name:
                    await message.reply(
                        "Sorry, I have never seen that user's message or user, so I am unable to fetch the ID."
                    )
                else:
                    await message.reply(
                        f"User {message.reply_to_message.from_user.first_name}'s ID is <code>{message.reply_to_message.from_user.id}</code>."
                    )
            else:
                # Proceed with the normal conditions if it's not a sticker
                if message.reply_to_message.forward_from_chat:
                    await message.reply(
                        f"The forwarded {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} has an ID of <code>{message.reply_to_message.forward_from_chat.id}</code>."
                    )
                elif message.reply_to_message.forward_from:
                    await message.reply(
                        f"The forwarded user, {message.reply_to_message.forward_from.first_name} has an ID of <code>{message.reply_to_message.forward_from.id}</code>."
                    )
                elif message.reply_to_message.forward_sender_name:
                    await message.reply(
                        "Sorry, I have never seen that user's message or user, so I am unable to fetch the ID."
                    )
                else:
                    await message.reply(
                        f"User {message.reply_to_message.from_user.first_name}'s ID is <code>{message.reply_to_message.from_user.id}</code>."
                    )
        else:
            if message.chat:
                await message.reply(
                    f"User {message.from_user.first_name}'s ID is <code>{message.from_user.id}</code>.\nThis chat's ID is: <code>{message.chat.id}</code>."
                )
            else:
                await message.reply(
                    f"User {message.from_user.first_name}'s ID is <code>{message.from_user.id}</code>."
                )
    except Exception:
        await message.reply("An error occurred while getting the ID.")


__MODULE__ = "ɪᴅ ғɪɴᴅᴇʀ"
__HELP__ = """
## ɪᴅ ғɪɴᴅᴇʀ 🆔

» `/id` : 
ɢᴇᴛ ᴛʜᴇ ɪᴅ ᴏꜰ ᴀ ᴜꜱᴇʀ, ᴄʜᴀᴛ, ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, ᴏʀ ꜱᴛɪᴄᴋᴇʀ ꜱᴇɴᴅᴇʀ.

✅ ᴡᴏʀᴋꜱ ɪɴ:
• ʀᴇᴘʟɪᴇᴅ ᴜꜱᴇʀꜱ
• ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ
• ɢʀᴏᴜᴘ / ᴄʜᴀɴɴᴇʟ / ᴘᴇʀꜱᴏɴᴀʟ ᴄʜᴀᴛꜱ
• ꜱᴛɪᴄᴋᴇʀ ᴍᴇꜱꜱᴀɢᴇꜱ
"""
