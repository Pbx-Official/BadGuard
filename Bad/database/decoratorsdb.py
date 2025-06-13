from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import SUPPORT_GROUP
from Bad.misc import SUDOERS

def AdminRightsCheck(mystic):
    async def wrapper(client: Client, message):
        # Check if user is a sudoer
        if message.from_user.id not in SUDOERS:
            # Check if user is admin in the chat
            try:
                member = await client.get_chat_member(message.chat.id, message.from_user.id)
                if not member.privileges or not member.privileges.can_manage_chat:
                    return await message.reply_text(
                        "You need admin rights to perform this action.",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Support", url=SUPPORT_GROUP)]]
                        )
                    )
            except:
                return await message.reply_text("Failed to check admin status.")

        # Delete the command message if possible
        try:
            await message.delete()
        except:
            pass

        # Execute the decorated function
        return await mystic(client, message)

    return wrapper
