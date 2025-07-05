from asyncio import sleep
from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import MessageDeleteForbidden, RPCError
from pyrogram.types import Message
from Bad import app
from Pbx import Owner

@app.on_message(filters.command("purge"))
async def purge(app: app, msg: Message):
    member = await msg.chat.get_member(msg.from_user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return 

    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ ᴍᴀᴋᴇ sᴜᴘᴇʀ ɢʀᴏᴜᴘ.**")
        return

    if msg.reply_to_message:
        message_ids = list(range(msg.reply_to_message.id, msg.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]


        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await app.delete_messages(chat_id=msg.chat.id, message_ids=plist, revoke=True)

            await msg.delete()
        except MessageDeleteForbidden:
            await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇssᴀɢᴇs. ᴛʜᴇ ᴍᴇssᴀɢᴇs ᴍᴀʏ ʙᴇ ᴛᴏᴏ ᴏʟᴅ, ɪ ᴍɪɢʜᴛ ɴᴏᴛ ʜᴀᴠᴇ ᴅᴇʟᴇᴛᴇ ʀɪɢʜᴛs, ᴏʀ ᴛʜɪs ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀ sᴜᴘᴇʀɢʀᴏᴜᴘ.**")
            return

        except RPCError as ef:
            await msg.reply_text(text=f"**sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ, **")
        count_del_msg = len(message_ids)
        sumit = await msg.reply_text(text=f"ᴅᴇʟᴇᴛᴇᴅ <i>{count_del_msg}</i> ᴍᴇssᴀɢᴇs")
        await sleep(3)
        await sumit.delete()
        return
    await msg.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢᴇ !**")
    return





@app.on_message(filters.command("spurge"))
async def spurge(app: app, msg: Message):
    member = await msg.chat.get_member(msg.from_user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return 
  

    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ ᴍᴀᴋᴇ sᴜᴘᴇʀ ɢʀᴏᴜᴘ.**")
        return

    if msg.reply_to_message:
        message_ids = list(range(msg.reply_to_message.id, msg.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await app.delete_messages(chat_id=msg.chat.id, message_ids=plist, revoke=True)
            await msg.delete()
        except MessageDeleteForbidden:
            await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇssᴀɢᴇs. ᴛʜᴇ ᴍᴇssᴀɢᴇs ᴍᴀʏ ʙᴇ ᴛᴏᴏ ᴏʟᴅ, ɪ ᴍɪɢʜᴛ ɴᴏᴛ ʜᴀᴠᴇ ᴅᴇʟᴇᴛᴇ ʀɪɢʜᴛs, ᴏʀ ᴛʜɪs ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀ sᴜᴘᴇʀɢʀᴏᴜᴘ.**")
            return

        except RPCError as ef:
            await msg.reply_text(text=f"**sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴜsɪɴɢ** `/bug`<b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>")           
            return        
    await msg.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢᴇ !**")
    return


@app.on_message(filters.command("del"))
async def del_msg(app: app, msg: Message):
    user = msg.from_user.id
    if user in Owner:
        pass
    else:
         member = await msg.chat.get_member(user)
         if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
             pass
         else:
             return 
    
    if msg.reply_to_message:
        await msg.delete()
        await app.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
    else:
        await msg.reply_text(text="**ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ.**")
        return

__MODULE__ = "ᴘᴜʀɢᴇ"
__HELP__ = """ 

## ᴘᴜʀɢᴇ ᴄᴏᴍᴍᴀɴᴅꜱ 🧹

» `/purge` : ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇꜱꜱᴀɢᴇꜱ ᴀꜰᴛᴇʀ ɪᴛ, ɪɴᴄʟᴜᴅɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴏɴᴇ.

» `/spurge` : ꜱᴀᴍᴇ ᴀꜱ `/purge`, ʙᴜᴛ ᴅᴏᴇꜱ ɴᴏᴛ ꜱᴇɴᴅ ᴀɴʏ ꜰɪɴᴀʟ ʀᴇᴘʟʏ ᴍᴇꜱꜱᴀɢᴇ. ᴄʟᴇᴀɴᴇʀ ᴠᴇʀꜱɪᴏɴ ꜰᴏʀ ꜱᴛᴇᴀʟᴛʜ ᴘᴜʀɢɪɴɢ.

» `/del` : ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɪᴛ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛʀɪɢɢᴇʀ.

❖ ʙᴏᴛ ᴍᴜꜱᴛ ʙᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ  
❖ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴏʀ ᴏᴡɴᴇʀꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜᴇꜱᴇ ᴄᴏᴍᴍᴀɴᴅꜱ  
❖ ᴡᴏʀᴋꜱ ᴏɴʟʏ ɪɴ ꜱᴜᴘᴇʀɢʀᴏᴜᴘꜱ  

"""
