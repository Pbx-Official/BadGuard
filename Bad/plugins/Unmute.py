import random
from pyrogram import filters, enums
from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)
from Bad import app
from Pbx import Owner
from config import *
from pyrogram.errors import RPCError
import requests 
from Bad.plugins.Ban import extract_user, mention


async def unmute_user(user_id, first_name, admin_id, admin_name, chat_id, message):
    try:
        member = await app.get_chat_member(chat_id, user_id)
        if member.status != enums.ChatMemberStatus.RESTRICTED:
            return "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴍᴜᴛᴇᴅ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ 🌾.", False
    except Exception as e:
        return f"Error occurred while checking user status: {e}", False

    try:
        await app.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(
                can_send_media_messages=True,
                can_send_messages=True,
                can_invite_users=True
            )
        )
    except ChatAdminRequired:
        msg_text = "ꜰɪʀꜱᴛ ɢɪᴠᴇ ᴍᴇ ᴍᴜᴛᴇ ʀɪɢʜᴛꜱ ᴛʜᴇɴ ᴜꜱᴇ ɪᴛ 🥺"
        return msg_text, False
    except Exception as e:
        msg_text = f"Oops!!\n{e}"
        return msg_text, False
    url = "https://api.waifu.pics/sfw/happy"
    response = requests.get(url).json()
    pimg = response['url']
    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    button = [
        [
            
            InlineKeyboardButton(
                text="• ᴅᴇʟᴇᴛᴇ •",
                callback_data=f"close",
            ),
        ]
    ]
    
    UNMUTEE = await message.reply_video(
        pimg,
        caption=f"<u>Uɴᴍᴜᴛᴇ Eᴠᴇɴᴛ </u>\n\n Nᴀᴍᴇ - {user_mention} \n Uɴᴍᴜᴛᴇᴅ Bʏ - {admin_mention}",
        reply_markup=InlineKeyboardMarkup(button),
    )
    return UNMUTEE, True


@app.on_message(filters.command(["unmute"]))
async def ban_command_handler(client, message):
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
        return await message.reply_text("User not found!")

    msg_text, result = await unmute_user(user_id, first_name, admin_id, admin_name, chat_id, message)
    if not result:
        await message.reply_text(msg_text)




@app.on_callback_query(filters.regex("^unmute_"))
async def unmutebutton(c: app, q: CallbackQuery):
    splitter = (str(q.data).replace("unmute_", "")).split("=")
    user_id = int(splitter[1])
    user = await q.message.chat.get_member(q.from_user.id)

    if not user:
        await q.answer(
            "You don't have enough permission to do this!\nStay in your limits!",
            show_alert=True,
        )
        return

    if not user.privileges.can_restrict_members and user.id != OWNER_ID:
        await q.answer(
            "You don't have enough permission to do this!\nStay in your limits!",
            show_alert=True,
        )
        return
    
    whoo = await c.get_users(user_id)
    
    try:
        await q.message.chat.unban_member(user_id)
    except RPCError as e:
        await q.message.edit_text(f"Error: {e}")
        return
    
    await q.message.edit_text(f"ᴜɴᴍᴜᴛᴇ ᴇᴠᴇɴᴛ \n\n ɴᴀᴍᴇ - {whoo.mention}! \nUɴᴍᴜᴛᴇᴅ Bʏ {q.from_user.mention}")
    return
