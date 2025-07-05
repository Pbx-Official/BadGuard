from pyrogram import enums
from pyrogram.enums import ChatType
from pyrogram import filters, Client
from Bad import app
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Pbx import Owner

@app.on_message(filters.command("pin"))
async def pin(_, message):
    replied = message.reply_to_message
    chat_title = message.chat.title
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat = message.chat
    name = message.from_user.mention
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ᴏɴ ɢʀᴏᴜᴘs !**")
    if not replied:
        await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴘɪɴ ɪᴛ !**")
    else:
        if user_id in Owner:
            pass
        else:
            member = await chat.get_member(user_id)
            if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                if member.privileges.can_pin_messages:
                    pass
                else:
                    msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ.."
                    return await message.reply_text(msg_text)
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ."
                return await message.reply_text(msg_text)
    await message.reply_to_message.pin()
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴘɪɴɴᴇᴅ\n\nʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ - {name}")
                

@app.on_message(filters.command("pinned"))
async def pinned(_, message):
    chat = await app.get_chat(message.chat.id)
    if not chat.pinned_message:
        return await message.reply_text("**ɴᴏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ ғᴏᴜɴᴅ**")
    try:        
        await message.reply_text("ʜᴇʀᴇ ɪs ᴛʜᴇ ʟᴀᴛᴇsᴛ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ",reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton(text="📝 ᴠɪᴇᴡ ᴍᴇssᴀɢᴇ",url=chat.pinned_message.link)]]))  
    except Exception as er:
        await message.reply_text(er)



@app.on_message(filters.command("unpin"))
async def unpin(_, message):
    replied = message.reply_to_message
    chat_title = message.chat.title
    chat_id = message.chat.id
    chat = mesaage.chat
    user_id = message.from_user.id
    name = message.from_user.mention

    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ᴏɴ ɢʀᴏᴜᴘs !**")
    if not replied:
        await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴜɴᴘɪɴ ɪᴛ !**")
    else:
        if user_id in Owner:
            pass
        else:
            member = await chat.get_member(user_id)
            if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                if member.privileges.can_pin_messages:
                    pass
                else:
                    msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ.."
                    return await message.reply_text(msg_text)
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ."
                return await message.reply_text(msg_text)
    await message.reply_to_message.unpin()
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴᴘɪɴɴᴇᴅ \n\nʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ - {name}")
                






@app.on_message(filters.command("removephoto"))
async def deletechatphoto(client, message):
    chat_id = message.chat.id
    chat = message.chat
    user_id = message.from_user.id
    name = message.from_user.mention
    msg = await message.reply_text("**ᴘʀᴏᴄᴇssɪɴɢ....**")
    admin_check = await message.chat.get_member(user_id)
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴ ɢʀᴏᴜᴘs!**")
        return
    
    if user_id in Owner:
        pass
    else:
        member = await chat.get_member(user_id)
        if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
            if member.privileges.can_change_info:
                pass
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.."
                return await message.reply_text(msg_text)
        else:
            msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
            return await message.reply_text(msg_text)
    
    await client.delete_chat_photo(chat_id)
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ᴄᴜʀʀᴇɴᴛ ᴘʜᴏᴛᴏ\n\nʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ - {name}")





@app.on_message(filters.command("setphoto"))
async def setchatphoto(client, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat = message.chat
    msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    admin_check = await message.chat.get_member(user_id)
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("`ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴ ɢʀᴏᴜᴘs!`")
        return
    
    if not reply:
        return await msg.edit("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴅᴏᴄᴜᴍᴇɴᴛ.**")
    
    if reply:
        if user_id in Owner:
            pass
        else:
            member = await chat.get_member(user_id)
            if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                if member.privileges.can_change_info:
                    pass
                else:
                    msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ.."
                    return await message.reply_text(msg_text)
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ."
                return await message.reply_text(msg_text)
    
    photo = await reply.download()
    await message.chat.set_photo(photo=photo)
    await message.reply_text(f"ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ɴᴇᴡ ᴘʜᴏᴛᴏ\n\nʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ {message.from_user.mention}")




from pyrogram import Client, filters, enums

@app.on_message(filters.command("settitle"))
async def setgrouptitle(client, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat = message.chat
    msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    
    if message.chat.type == enums.ChatType.PRIVATE:
        return await msg.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴ ɢʀᴏᴜᴘs!**")
    
    if message.reply_to_message and message.reply_to_message.text:
        title = message.reply_to_message.text
        admin_check = await message.chat.get_member(user_id)
        
        if user_id in Owner:  # Assuming `Owner` is a list of user IDs
            pass
        else:
            member = await chat.get_member(user_id)
            if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                if member.privileges.can_change_info:
                    pass
                else:
                    msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.."
                    return await message.reply_text(msg_text)
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
                return await message.reply_text(msg_text)
        
        await message.chat.set_title(title)
        await msg.edit(f"**sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ɴᴇᴡ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ!\nʙʏ** {message.from_user.mention}")
    
    elif len(message.command) > 1:
        title = message.text.split(None, 1)[1]
        
        if user_id in Owner:  # Assuming `Owner` is a list of user IDs
            pass
        else:
            member = await chat.get_member(user_id)
            if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                if member.privileges.can_change_info:
                    pass
                else:
                    msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.."
                    return await message.reply_text(msg_text)
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
                return await message.reply_text(msg_text)
        
        await message.chat.set_title(title)
        await msg.edit(f"**sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ɴᴇᴡ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ!\nʙʏ** {message.from_user.mention}")
    
    else:
        await msg.edit("**ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ**")


@app.on_message(filters.command("setdiscription"))
async def setg_discription(client, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    chat = message.chat
    user_id = message.from_user.id
    msg = await message.reply_text("**ᴘʀᴏᴄᴇssɪɴɢ...**")
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴ ɢʀᴏᴜᴘs!**")
        return
    
    if message.reply_to_message and message.reply_to_message.text:
        discription = message.reply_to_message.text
        
        if user_id in Owner:
            pass
        else:
            member = await chat.get_member(user_id)
            if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                if member.privileges.can_change_info:
                    pass
                else:
                    msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.."
                    return await message.reply_text(msg_text)
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
                return await message.reply_text(msg_text)
        
        await message.chat.set_description(discription)
        await msg.edit(f"**sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ɴᴇᴡ ɢʀᴏᴜᴘ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ!\nʙʏ** {message.from_user.mention}")
    
    elif len(message.command) > 1:
        discription = message.text.split(None, 1)[1]
        
        if user_id in Owner:
            pass
        else:
            member = await chat.get_member(user_id)
            if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                if member.privileges.can_change_info:
                    pass
                else:
                    msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.."
                    return await message.reply_text(msg_text)
            else:
                msg_text = "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
                return await message.reply_text(msg_text)
        
        await message.chat.set_description(discription)
        await msg.edit(f"**sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ɴᴇᴡ ɢʀᴏᴜᴘ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ!\nʙʏ** {message.from_user.mention}")
    
    else:
        await msg.edit("**ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ!**")


@app.on_message(filters.command(["admins","staff"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == enums.ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**ɢʀᴏᴜᴘ sᴛᴀғғ - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 ᴏᴡɴᴇʀ\n└ {owner.mention}\n\n👮🏻 ᴀᴅᴍɪɴs\n"
      else:
        text2 += f"👑 ᴏᴡɴᴇʀ\n└ @{owner.username}\n\n👮🏻 ᴀᴅᴍɪɴs\n"
    except:
      text2 += f"👑 ᴏᴡɴᴇʀ\n└ <i>Hidden</i>\n\n👮🏻 ᴀᴅᴍɪɴs\n"
    if len(adminList) == 0:
      text2 += "└ <i>ᴀᴅᴍɪɴs ᴀʀᴇ ʜɪᴅᴅᴇɴ</i>"  
      await app.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ᴀᴅᴍɪɴs**: {lenAdminList}"  
      await app.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       


@app.on_message(filters.command("bots"))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"**ʙᴏᴛ ʟɪsᴛ - {message.chat.title}**\n\n🤖 ʙᴏᴛs\n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"├ @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅ | *ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ʙᴏᴛs**: {lenBotList}"  
      await app.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)


__MODULE__ = "ɢʀᴏᴜᴘ ᴄᴍᴅ"
__HELP__ = """ 

## ɢʀᴏᴜᴘ ᴄᴏᴍᴍᴀɴᴅꜱ 🧩

» `/pin` : ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴘɪɴ ɪᴛ
» `/pinned` : ᴄʜᴇᴄᴋ ᴛʜᴇ ʟᴀꜱᴛ ᴘɪɴɴᴇᴅ ᴍᴇꜱꜱᴀɢᴇ
» `/unpin` : ᴜɴᴘɪɴ ᴀ ᴍᴇꜱꜱᴀɢᴇ ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ɪᴛ

» `/staff` : ɢᴇᴛ ᴀ ʟɪꜱᴛ ᴏꜰ ᴀʟʟ ꜱᴛᴀꜰꜰ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ
» `/bots` : ᴄʜᴇᴄᴋ ᴀʟʟ ʙᴏᴛꜱ ᴀᴅᴅᴇᴅ ɪɴ ɢʀᴏᴜᴘ

» `/settitle` : ꜱᴇᴛ ᴀ ɴᴇᴡ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ
» `/setdescription` : ᴄʜᴀɴɢᴇ ᴛʜᴇ ɢʀᴏᴜᴘ'ꜱ ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ
» `/setphoto` : ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ ᴛᴏ ꜱᴇᴛ ɪᴛ ᴀꜱ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ
» `/removephoto` : ʀᴇᴍᴏᴠᴇ ᴄᴜʀʀᴇɴᴛ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ

"""
