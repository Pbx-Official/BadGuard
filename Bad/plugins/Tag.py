import asyncio
from Bad import app
from pyrogram import filters


SPAM_CHATS = []


@app.on_message(filters.command(["mention", "utag", "all"]) & filters.group)
async def tag_all_users(_,message): 
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:
        await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ**") 
        return                  
    if replied:
        SPAM_CHATS.append(message.chat.id)      
        usernum= 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id): 
            if message.chat.id not in SPAM_CHATS:
                break       
            usernum += 3
            usertxt += f"\n⚘ [{m.user.first_name}](tg://user?id={m.user.id})\n"
            if usernum == 1:
                await replied.reply_text(usertxt)
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        try :
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        text = message.text.split(None, 1)[1]

        SPAM_CHATS.append(message.chat.id)
        usernum= 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id):       
            if message.chat.id not in SPAM_CHATS:
                break 
            usernum += 1
            usertxt += f"\n⚘ [{m.user.first_name}](tg://user?id={m.user.id})\n"
            if usernum == 3:
                await app.send_message(message.chat.id,f'{text}\n{usertxt}')
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""                          
        try :
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass        

@app.on_message(filters.command(["mantionoff", "tagstop", "cancel", "stop"]))
async def cancelcmd(_, message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try :
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass   
        return await message.reply_text("**ᴛᴀɢ ᴀʟʟ sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴏᴘᴘᴇᴅ!**")     

    else :
        await message.reply_text("**ɴᴏ ᴘʀᴏᴄᴇss ᴏɴɢᴏɪɴɢ!**")  
        return       


@app.on_message(filters.command("admin") | (filters.text & filters.regex(r"@admin")) & filters.group)
async def tag_admins(_, message):
    # Check if the command is in reply or with extra text
    replied = message.reply_to_message
    chat_id = message.chat.id
    admin_list = []
    async for member in app.get_chat_members(chat_id, filter="administrators"):
        # Ignore bots
        if member.user.is_bot:
            continue
        admin_list.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
    if not admin_list:
        await message.reply_text("No admins found in this group.")
        return

    admin_tags = " ".join(admin_list)
    if replied:
        await replied.reply_text(
            f"**Reported to admins.**\n{admin_tags}"
        )
    else:
        await message.reply_text(
            f"**Reported to admins.**\n{admin_tags}"
        )


__MODULE__ = "ᴀᴅᴍɪɴ ᴜᴛᴀɢ"
__HELP__ = """

## 👥 ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ

» `/mention <text>` | `/utag` | `/all <text>`  
• ᴛᴀɢ ᴀʟʟ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀꜱ ᴡɪᴛʜ ᴄᴜꜱᴛᴏᴍ ᴍᴇꜱꜱᴀɢᴇ  
• ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ꜱᴇɴᴅ ᴛᴀɢs ᴜɴᴅᴇʀ ᴀ ʀᴇᴘʟʏ

» `/stop` | `/cancel` | `/tagstop` | `/mantionoff`  
• sᴛᴏᴘ ᴏɴɢᴏɪɴɢ ᴛᴀɢ ᴀʟʟ ᴘʀᴏᴄᴇss

❖ ᴜꜱᴇꜰᴜʟ ᴛᴏ ɢʀᴀʙ ᴀᴛᴛᴇɴᴛɪᴏɴ ᴏꜰ ᴀʟʟ ᴜꜱᴇʀꜱ  
❖ 3 ᴍᴇᴍʙᴇʀꜱ ᴘᴇʀ ᴍᴇssᴀɢᴇ (ᴛᴏ ᴀᴠᴏɪᴅ ꜰʟᴏᴏᴅ ʟɪᴍɪᴛs)

---

## 👮 ᴀᴅᴍɪɴ ᴛᴀɢɢɪɴɢ

» `/admin` or ᴛʏᴘᴇ `@admin` ɪɴ ᴀ ᴍᴇssᴀɢᴇ  
• ᴛᴀɢ ᴀʟʟ ᴀᴅᴍɪɴs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ  
• ᴡᴏʀᴋs ɪɴ ʀᴇᴘʟʏ ᴏʀ sᴛᴀɴᴅᴀʟᴏɴᴇ

❖ ɢʀᴇᴀᴛ ꜰᴏʀ ʀᴇᴘᴏʀᴛɪɴɢ ᴜɴᴅᴇʀ ʀᴜʟᴇ ʙʀᴇᴀᴋs
"""
