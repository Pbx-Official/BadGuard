import os
from PIL import Image, ImageDraw, ImageFont
import requests
import random 
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Bad.database.pretenderdb import impo_off, impo_on, check_pretender, add_userdata, get_userdata, usr_data
from Bad import app
from Bad.database import ZeroTwo


BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ᴋɪᴅɴᴀᴘ ᴍᴇ",
                url=f"https://t.me/{app.username}?startgroup=new",
            ),
            InlineKeyboardButton(
                text="ᴄʟᴏsᴇ ",
                callback_data="close",
            )
        ]
    ]
)


async def download_pic(user_id):
    user = await app.get_users(user_id)
    if user.photo:
        file_path = await app.download_media(user.photo.big_file_id)
        return file_path
    else:
        return "assets/NODP.PNG"

async def genimposterimg(user_id, username, first_name, thumb):
    photo_path = await download_pic(user_id)
    background = Image.open(f"resources/image/I/{thumb}.png")
    user_photo = Image.open(photo_path)
    user_photo = user_photo.resize((900, 900))
    mask = Image.new("L", (900, 900), 0) 
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 900, 900), fill=255)
    user_photo.putalpha(mask.resize(user_photo.size))  
    background.paste(user_photo, (223, 317), user_photo) 
    draw = ImageDraw.Draw(background)

    impostor_path = f"impostor_{user_id}.png"
    background.save(impostor_path)

    return impostor_path



@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    if message.sender_chat or not await check_pretender(message.chat.id):
        return
    thumb = random.choice(ZeroTwo)
    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    usernamebefore, first_name, lastname_before = await get_userdata(message.from_user.id)
    msg = ""
    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"""
**ᴜsᴇʀ sʜᴏʀᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ **

**๏ ɴᴀᴍᴇ** ➛ {message.from_user.mention}
**๏ ᴜsᴇʀ ɪᴅ** ➛ {message.from_user.id}
"""
    if usernamebefore != message.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else "NO USERNAME"
        usernameafter = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else "NO USERNAME"
        )
        msg += """
** ᴄʜᴀɴɢᴇᴅ ᴜsᴇʀɴᴀᴍᴇ **

**๏ ᴡɪᴛʜᴏᴜᴛ ᴄʜᴀɴɢᴇ ᴜsᴇʀɴᴀᴍᴇ** ➛ {bef}
**๏ ᴀғᴛᴇʀ ᴄʜᴀɴɢᴇ ᴜsᴇʀɴᴀᴍᴇ** ➛ {aft}
""".format(bef=usernamebefore, aft=usernameafter)
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if first_name != message.from_user.first_name:
        msg += """
** ᴄʜᴀɴɢᴇs ғɪʀsᴛ ɴᴀᴍᴇ **

**๏ ᴡɪᴛʜᴏᴜᴛ ᴄʜᴀɴɢᴇ ғʀɪsᴛ ɴᴀᴍᴇ** ➛ {bef}
**๏ ᴀғᴛᴇʀ ᴄʜᴀɴɢᴇ ғʀɪsᴛ ɴᴀᴍᴇ** ➛ {aft}
""".format(
            bef=first_name, aft=message.from_user.first_name
        )
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if lastname_before != message.from_user.last_name:
        lastname_before = lastname_before or "NO LAST NAME"
        lastname_after = message.from_user.last_name or "NO LAST NAME"
        msg += """
**ᴄʜᴀɴɢᴇs ʟᴀsᴛ ɴᴀᴍᴇ **

**๏ ᴡɪᴛʜᴏᴜᴛ ᴄʜᴀɴɢᴇ ʟᴀsᴛ ɴᴀᴍᴇ** ➛ {bef}
**๏ ᴀғᴛᴇʀ ᴄʜᴀɴɢᴇ ʟᴀsᴛ ɴᴀᴍᴇ** ➛ {aft}
""".format(
            bef=lastname_before, aft=lastname_after
        )
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if msg != "":
        Imposterimg = await genimposterimg(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            thumb,
        )
        await message.reply_photo(Imposterimg, caption=msg, reply_markup=BUTTON)

# HEHE
@app.on_message(filters.group & filters.command("imposter") & ~filters.bot & ~filters.via_bot)
async def set_mataa(_, message: Message):
    if len(message.command) == 1:
        return await message.reply("**ᴅᴇᴛᴇᴄᴛ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴇʀs ᴜsᴀɢᴇ ** \n /imposter enable or disable")
    if message.command[1] == "enable":
        cekset = await impo_on(message.chat.id)
        if cekset:
            await message.reply("**ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
        else:
            await impo_on(message.chat.id)
            await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴀʙʟᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ғᴏʀ** {message.chat.title}")
    elif message.command[1] == "disable":
        cekset = await impo_off(message.chat.id)
        if not cekset:
            await message.reply("**ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.**")
        else:
            await impo_off(message.chat.id)
            await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀʙʟᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ғᴏʀ** {message.chat.title}")
    else:
        await message.reply("**ᴅᴇᴛᴇᴄᴛ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴇʀs ᴜsᴀɢᴇ : ᴘʀᴇᴛᴇɴᴅᴇʀ enable|disable**")

__MODULE__ = "ɪᴍᴘᴏꜱᴛᴇʀ"
__HELP__ = """ 

## ɪᴍᴘᴏꜱᴛᴇʀ 🕵️

» `/imposter [enable | disable]` :
ᴛʜɪꜱ ᴛᴏɢɢʟᴇꜱ ᴛʜᴇ **ɪᴍᴘᴏꜱᴛᴇʀ ᴅᴇᴛᴇᴄᴛɪᴏɴ** ꜰᴇᴀᴛᴜʀᴇ.

• ᴡʜᴇɴ ᴀ ᴜꜱᴇʀ ᴄʜᴀɴɢᴇꜱ ᴛʜᴇɪʀ:
  - ꜰɪʀꜱᴛ ɴᴀᴍᴇ
  - ʟᴀꜱᴛ ɴᴀᴍᴇ
  - ᴜꜱᴇʀɴᴀᴍᴇ

» ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ꜱᴇɴᴅ ᴀ ꜱᴛʏʟɪꜱʜ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴ ᴛʜᴜᴍʙɴᴀɪʟ ᴡɪᴛʜ ᴛʜᴇɪʀ ɴᴇᴡ ᴅᴇᴛᴀɪʟꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.

"""
