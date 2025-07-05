from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.types import (
    CallbackQuery,
    Chat,
    ChatJoinRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Bad import app
from Bad.core.mongo import mongodb
from Bad.misc import SUDOERS

approvaldb = mongodb.autoapprove

def build_keyboard(buttons):
    keyboard = [
        [InlineKeyboardButton(text, callback_data=data) for text, data in buttons.items()]
    ]
    return InlineKeyboardMarkup(keyboard)

@app.on_message(filters.command("autoapprove") & filters.group)
async def approval_command(client, message: Message):
    chat_id = message.chat.id
    chat = message.chat
    admin_id = message.from_user.id
    member = await chat.get_member(admin_id)
    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        if member.privileges.can_restrict_members:
            chat = await approvaldb.find_one({"chat_id": chat_id})
            if chat:
                mode = chat.get("mode", "")
                if not mode:
                    mode = "automatic"
                    await approvaldb.update_one(
                        {"chat_id": chat_id},
                        {"$set": {"mode": mode}},
                        upsert=True,
                    )
                if mode == "automatic":
                    switch = "manual"
                else:
                    switch = "automatic"
                buttons = {
                    "ᴅᴇꜱᴀʙʟᴇ": "approval_off",
                    f"{mode.upper()}": f"approval_{switch}",
                }
                keyboard = build_keyboard(buttons)
                await message.reply(
                    f"ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇʟ ꜰᴏʀ {message.chat.title} ɪꜱ \n<u>ᴇɴᴀʙʟᴇᴅ</u>", reply_markup=keyboard
                )
            else:
                buttons = {"ᴇɴᴀʙʟᴇ": "approval_on"}
                keyboard = build_keyboard(buttons)
                await message.reply(
                    f"ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇʟ ꜰᴏʀ {message.chat.title} ɪꜱ \n<u>ᴅᴇꜱᴀʙʟᴇᴅ </u>", reply_markup=keyboard
                )
        else:
            msg_text = "ꜱᴏʀʀʏ ᴍʏ ᴅᴀʀʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ 🌟"
            await message.reply_text(msg_text)
    else:
        msg_text = "ꜱᴏʀʀʏ ᴍʏ ᴅᴀʀʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ 🌟"
        await message.reply_text(msg_text)

@app.on_callback_query(filters.regex("approval(.*)"))
async def approval_cb(client, cb: CallbackQuery):
    chat_id = cb.message.chat.id
    from_user = cb.from_user
    chat = cb.message.chat
    admin_id = from_user.id
    member = await chat.get_member(admin_id)
    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        if member.privileges.can_restrict_members:
            command_parts = cb.data.split("_", 1)
            option = command_parts[1]
            if option == "off":
                if await approvaldb.count_documents({"chat_id": chat_id}) > 0:
                    await approvaldb.delete_one({"chat_id": chat_id})
                    buttons = {"ᴇɴᴀʙʟᴇ ": "approval_on"}
                    keyboard = build_keyboard(buttons)
                    return await cb.edit_message_text(
                        f"ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇʟ ꜰᴏʀ {cb.message.chat.title} ɪꜱ \n<u> ᴅᴇꜱᴀʙʟᴇᴅ </u>", reply_markup=keyboard,
                    )
            if option == "on":
                switch = "manual"
                mode = "automatic"
            if option == "automatic":
                switch = "manual"
                mode = option
            if option == "manual":
                switch = "automatic"
                mode = option
            await approvaldb.update_one(
                {"chat_id": chat_id},
                {"$set": {"mode": mode}},
                upsert=True,
            )
            chat = await approvaldb.find_one({"chat_id": chat_id})
            mode = chat["mode"].upper()
            buttons = {"Turn OFF": "approval_off", f"{mode}": f"approval_{switch}"}
            keyboard = build_keyboard(buttons)
            await cb.edit_message_text(
                f"ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇʟ ꜰᴏʀ {cb.message.chat.title} ɪꜱ \n<u> ᴇɴᴀʙʟᴇᴅ </u>", reply_markup=keyboard
            )
        else:
            msg_text = "ꜱᴏʀʀʏ ᴍʏ ᴅᴀʀʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ 🌟"
            await cb.message.reply_text(msg_text)
    else:
        msg_text = "ꜱᴏʀʀʏ ᴍʏ ᴅᴀʀʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ 🌟"
        await cb.message.reply_text(msg_text)

@app.on_message(filters.command("clear_pending") & filters.group)
async def clear_pending_command(client, message: Message):
    chat_id = message.chat.id
    chat = message.chat
    admin_id = message.from_user.id
    member = await chat.get_member(admin_id)
    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        if member.privileges.can_restrict_members:
            result = await approvaldb.update_one(
                {"chat_id": chat_id},
                {"$set": {"pending_users": []}},
            )
            if result.modified_count > 0:
                await message.reply_text("ᴄʟᴇᴀʀᴇᴅ ᴘᴇɴᴅɪɴɢ ᴜꜱᴇʀꜱ....")
            else:
                await message.reply_text("ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴘᴇɴᴅɪɴɢ ᴜꜱᴇʀꜱ ᴛᴏ ᴄʟᴇᴀʀ ....")
        else:
            msg_text = "ꜱᴏʀʀʏ ᴍʏ ᴅᴀʀʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ 🌟"
            await message.reply_text(msg_text)
    else:
        msg_text = "ꜱᴏʀʀʏ ᴍʏ ᴅᴀʀʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ 🌟"
        await message.reply_text(msg_text)

@app.on_chat_join_request(filters.group)
async def accept(client, request: ChatJoinRequest):
    chat = request.chat
    user = request.from_user
    chat_data = await approvaldb.find_one({"chat_id": chat.id})
    if chat_data:
        mode = chat_data["mode"]
        if mode == "automatic":
            await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
            return
        if mode == "manual":
            is_user_in_pending = await approvaldb.count_documents(
                {"chat_id": chat.id, "pending_users": int(user.id)}
            )
            if is_user_in_pending == 0:
                await approvaldb.update_one(
                    {"chat_id": chat.id},
                    {"$addToSet": {"pending_users": int(user.id)}},
                    upsert=True,
                )
                buttons = {
                    "ᴀᴄᴄᴇᴘᴛ ": f"manual_approve_{user.id}",
                    "ᴅᴇᴄʟɪɴᴇ ": f"manual_decline_{user.id}",
                }
                keyboard = build_keyboard(buttons)
                text = f"ᴜꜱᴇʀ: {user.mention}\nSᴇɴᴛ ᴀ Jᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴀɴʏ ᴀᴅᴍɪɴ ᴄᴀɴ ᴀᴄᴄᴇᴘᴛ ᴏʀ ᴅᴇᴄʟɪɴᴇ ᴛʜᴇ ʀᴇǫᴜᴇsᴛ..\n\nᴘᴏᴡᴇʀᴇᴅ ʙʏ  {app.mention}"
                admin_data = [
                    i
                    async for i in client.get_chat_members(
                        chat_id=chat.id,
                        filter=ChatMembersFilter.ADMINISTRATORS,
                    )
                ]
                for admin in admin_data:
                    if admin.user.is_bot or admin.user.is_deleted:
                        continue
                    text += f"[\u2063](tg://user?id={admin.user.id})"
                await client.send_message(chat.id, text, reply_markup=keyboard)


@app.on_callback_query(filters.regex("manual_(.*)"))
async def manual(client, cb: CallbackQuery):
    chat = cb.message.chat
    from_user = cb.from_user
    admin_id = from_user.id
    member = await chat.get_member(admin_id)
    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        if member.privileges.can_restrict_members:
            datas = cb.data.split("_", 2)
            action = datas[1]
            user_id = int(datas[2])
            if action == "approve":
                await client.approve_chat_join_request(chat_id=chat.id, user_id=user_id)
            if action == "decline":
                await client.decline_chat_join_request(chat_id=chat.id, user_id=user_id)
            await approvaldb.update_one(
                {"chat_id": chat.id},
                {"$pull": {"pending_users": user_id}},
            )
            await cb.message.delete()
        else:
            msg_text = "ꜱᴏʀʀʏ ᴍʏ ᴅᴀʀʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ 🌟"
            await cb.message.reply_text(msg_text)
    else:
        msg_text = "ꜱᴏʀʀʏ ᴍʏ ᴅᴀʀʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴅᴏ ᴛʜɪꜱ 🌟"
        await cb.message.reply_text(msg_text)

__MODULE__ = "ᴀᴜᴛᴏᴀᴘᴘʀᴏᴠᴇ"
__HELP__ = """ 

## ᴀᴜᴛᴏᴀᴘᴘʀᴏᴠᴇ

» `/autoapprove` : ᴇɴᴀʙʟᴇ/ᴅɪꜱᴀʙʟᴇ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ꜰᴏʀ ᴄʜᴀᴛ ᴊᴏɪɴ ʀᴇǫᴜᴇꜱᴛꜱ

**ᴍᴏᴅᴇꜱ:**
• `Automatic` : ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴄᴄᴇᴘᴛꜱ ᴄʜᴀᴛ ᴊᴏɪɴ ʀᴇǫᴜᴇꜱᴛꜱ.
• `Manual` : ᴛᴀɢꜱ ᴀᴅᴍɪɴꜱ ꜰᴏʀ ᴍᴀɴᴜᴀʟ ᴀᴘᴘʀᴏᴠᴀʟ ᴏʀ ʀᴇᴊᴇᴄᴛɪᴏɴ.

» `/clearpending` : ᴄʟᴇᴀʀꜱ ᴀʟʟ ᴘᴇɴᴅɪɴɢ ᴜꜱᴇʀ ɪᴅꜱ ꜰʀᴏᴍ ᴅᴀᴛᴀʙᴀꜱᴇ, ᴀʟʟᴏᴡɪɴɢ ᴛʜᴇᴍ ᴛᴏ ʀᴇꜱᴇɴᴅ ʀᴇǫᴜᴇꜱᴛꜱ

"""
