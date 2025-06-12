import random
import asyncio
from pyrogram import Client, filters, enums
import datetime
from Bad import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
from Bad.database.nightmodedb import nightdb, nightmode_on, nightmode_off, get_nightchats


CLOSE_CHAT = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_change_info=False,
    can_add_web_page_previews=False,
    can_pin_messages=False,
    can_invite_users=False
)

OPEN_CHAT = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=True,
    can_add_web_page_previews=True,
    can_pin_messages=True,
    can_invite_users=True
)

buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("ᴇɴᴀʙʟᴇ", callback_data="add_night"),
     InlineKeyboardButton("ᴅɪsᴀʙʟᴇ", callback_data="rm_night")]
])


@app.on_message(filters.command("nightmode") & filters.group)
async def _nightmode(_, message):
    return await message.reply_photo(
        photo="https://telegra.ph/file/91370f62c00ccc0c69841.jpg",
        caption="**ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ɴɪɢʜᴛᴍᴏᴅᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**",
        reply_markup=buttons
    )


@app.on_callback_query(filters.regex("^(add_night|rm_night)$"))
async def nightcb(_, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    check_night = await nightdb.find_one({"chat_id": chat_id})
    administrators = []
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m.user.id)
    if user_id in administrators:
        if data == "add_night":
            if check_night:
                await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")
            elif not check_night:
                await nightmode_on(chat_id)
                await query.message.edit_caption("**๏ ᴀᴅᴅᴇᴅ ᴄʜᴀᴛ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ. ᴛʜɪs ɢʀᴏᴜᴘ ᴡɪʟʟ ʙᴇ ᴄʟᴏsᴇᴅ ᴏɴ 𝟷𝟸ᴀᴍ [IST] ᴀɴᴅ ᴡɪʟʟ ᴏᴘᴇɴᴇᴅ ᴏɴ 𝟶𝟼ᴀᴍ [IST].**")
        if data == "rm_night":
            if check_night:
                await nightmode_off(chat_id)
                await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ!**")
            elif not check_night:
                await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")


async def start_nightmode():
    chats = await get_nightchats()
    for chat in chats:
        chat_id = int(chat["chat_id"])
        try:
            await app.send_photo(
                chat_id,
                photo="https://telegra.ph/file/83a4c8921c49934558542.jpg",
                caption="**Bᴇғᴏʀᴇ ʏᴏᴜ ɢᴏ ᴛᴏ sʟᴇᴇᴘ\nᴅᴏ ɴᴏᴛ ғᴏʀɢᴇᴛ ᴛᴏ sᴀʏ ᴛʜᴀɴᴋs ғᴏʀ ᴇᴠᴇʀʏᴛʜɪɴɢ ɢᴏᴏᴅ ᴛʜᴀᴛ ʜᴀs ʜᴀᴘᴘᴇɴᴇᴅ ᴛᴏ ʏᴏᴜ ɪɴ ᴛʜᴇ ʟᴀsᴛ 𝟸𝟺 ʜᴏᴜʀs. I ᴀᴍ ᴛʜᴀɴᴋғᴜʟ ᴀᴛ ᴛʜᴇ ᴍᴏᴍᴇɴᴛ ғᴏʀ ʏᴏᴜ**"
            )
            await app.set_chat_permissions(chat_id, CLOSE_CHAT)
        except Exception as e:
            print(f"Unable to close Group {chat_id} - {e}")


async def close_nightmode():
    chats = await get_nightchats()
    for chat in chats:
        chat_id = int(chat["chat_id"])
        try:
            await app.send_photo(
                chat_id,
                photo="https://telegra.ph/file/d289562698b698711c3cd.jpg",
                caption="**Nᴏ ᴍᴀᴛᴛᴇʀ ʜᴏᴡ ʙᴀᴅ ᴛʜɪɴɢs ᴀʀᴇ, ʏᴏᴜ ᴄᴀɴ ᴀᴛ ʟᴇᴀsᴛ ʙᴇ ʜᴀᴘᴘʏ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴏᴋᴇ ᴜᴘ ᴛʜɪs ᴍᴏʀɴɪɴɢ**"
            )
            await app.set_chat_permissions(chat_id, OPEN_CHAT)
        except Exception as e:
            print(f"Unable to open Group {chat_id} - {e}")


async def nightmode_scheduler():
    while True:
        now = datetime.datetime.now()
        # Calculate the time until the next midnight (IST)
        midnight = datetime.datetime.combine(now.date(), datetime.time(23, 59, 0))
        if now > midnight:
            midnight += datetime.timedelta(days=1)
        time_to_midnight = (midnight - now).total_seconds()

        # Sleep until midnight
        await asyncio.sleep(time_to_midnight)

        # Start nightmode
        await start_nightmode()

        # Sleep until 6:01 AM IST
        time_to_morning = (datetime.datetime.combine(midnight.date(), datetime.time(6, 1, 0)) - datetime.datetime.now()).total_seconds()
        await asyncio.sleep(time_to_morning)

        # Close nightmode
        await close_nightmode()


asyncio.create_task(nightmode_scheduler())

    
    
