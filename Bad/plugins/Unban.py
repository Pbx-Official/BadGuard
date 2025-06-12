from pyrogram import filters, enums, client 
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)
import requests
from Bad import app
import datetime
from Pbx import Owner
import random 
from Bad.plugins.Ban import extract_user, mention
from pyrogram.errors import UserNotParticipant
from config import LOG_GROUP_ID, OWNER_ID
from pyrogram.types import *

async def unban_user(user_id, first_name, admin_id, admin_name, chat_id, message):
    member = await app.get_chat_member(chat_id, user_id)
    if member.status == enums.ChatMemberStatus.BANNED:
        pass
    else:
       msg = "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ʙᴀɴɴᴇᴅ "
       return msg 
        
    
    try:
        
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        msg_text = "ɢɪᴠᴇ ᴍᴇ ʙᴀɴ ʀɪɢʜᴛꜱ ᴛʜᴇɴ ᴜꜱᴇ ᴛʜɪꜱ"
        return msg_text
    except Exception as e:
        await app.send_message(LOG_GROUP_ID, f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ in unban!\n{e}")
        
        return 
    
    url = "https://api.waifu.pics/sfw/happy"
    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    button = [
       [
            
           InlineKeyboardButton(
               text="ᴄʟᴏꜱᴇ",
               callback_data=f"close",
           ),
        ]
    ]
    response = requests.get(url).json()
    pimg = response['url']
    await app.send_message(LOG_GROUP_ID, f"{user_mention} was unbanned by {admin_mention} in {message.chat.title}")
    caption = f"<u>ᴜɴʙᴀɴ ᴇᴠᴇɴᴛ</u>\n\nɴᴀᴍᴇ - {user_mention} \nᴜɴʙᴀɴɴᴇᴅ ʙʏ {admin_mention}"
    # Truncate the caption if it exceeds the Telegram message length limit
    if len(caption) > 4096:
        caption = caption[:4096] + "..."
    await message.reply_video(
        pimg,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(button)
    )
    return True 


  


@app.on_message(filters.command(["unban"]))
async def unban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    if admin_id in Owner:
        pass
    else:
        member = await chat.get_member(admin_id)
        if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
            if member.privileges.can_restrict_members:
                pass
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ.."
                return await message.reply_text(msg_text)
        else:
            msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ."
            return await message.reply_text(msg_text)

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        reason = None
    else:
        user_id, first_name, _ = await extract_user(client, message)
        reason = message.text.partition(message.command[1])[2] if len(message.command) > 1 else None

    if user_id is None:
        return await message.reply_text("ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ... ")



    msg_text, result = await unban_user(user_id, first_name, admin_id, admin_name, chat_id, message)
    if result:
        await message.reply_text(msg_text)
    else:
        await message.reply_text("Failed to unban the user.")



@app.on_callback_query(filters.regex("^unban_"))
async def unbanbutton(c: app, cb: CallbackQuery):
    splitter = (str(cb.data).replace("unban_", "")).split("=")
    user_id = int(splitter[1])
    user = await cb.message.chat.get_member(cb.from_user.id)

    if not user:
        await cb.answer(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ..",
            show_alert=True,
        )
        return

    if not user.privileges.can_restrict_members and cb.from_user.id != Owner:
        await cb.answer(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ..",
            show_alert=True,
        )
        return
    whoo = await c.get_chat(user_id)
    doneto = whoo.first_name if whoo.first_name else whoo.title
    try:
        await cb.message.chat.unban_member(user_id)
    except RPCError as e:
        await cb.message.edit_text(f"Error: {e}")
        return
    await cb.message.edit_text(f"<u>ᴜɴʙᴀɴ ᴇᴠᴇɴᴛ </u>\n\nɴᴀᴍᴇ - {doneto}\nᴜɴʙᴀɴɴᴇᴅ ʙʏ - {cb.from_user.mention}!")
    return
