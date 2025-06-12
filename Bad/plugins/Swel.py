import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageChops
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from Bad import app
from Bad.database import ZeroTwo

async def is_admin(chat_id: int, user_id: int) -> bool:
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    
motor_client = AsyncIOMotorClient(MONGO_DB_URI)
nos_wel_db = motor_client["nosweldatabase"]["disabled_chats"]

def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chat, id, uname, Thumbnail):
    background = Image.open(f"assets/ZeroTwo/{Thumbnail}.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((900, 900))
    draw = ImageDraw.Draw(background)
    font2 = ImageFont.truetype('assets/font.ttf', size=50)
  #  draw.text((48, 37), f"Zero Two", fill="orange", font=font2)
    pfp_position = (223, 317)  
    background.paste(pfp, pfp_position, pfp)
    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"

@app.on_message(filters.command("wel off") & filters.group)
async def disable_welcome(client, message):
    chat_id = message.chat.id
    
    if not is_admin:
        await message.reply_text("You need to be an admin to disable welcome messages.")
        return

    if await nos_wel_db.find_one({"chat_id": chat_id}):
        await message.reply_text("Special Welcome already Disabled.")
    else:
        await nos_wel_db.insert_one({"chat_id": chat_id})
        await message.reply_text("Special Welcome has been Disabled.")

@app.on_chat_member_updated(filters.group)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    xyz = await nos_wel_db.find_one({"chat_id": chat_id})
    if xyz: 
        return
    else:
        pass

    

    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    Thumbnail = random.choice(ZeroTwo)

    try:
        pic = await app.download_media(user.photo.big_file_id, file_name=f"pp{user.id}.png")
    except Exception:
        pic = "assets/NODP.PNG"

    try:
        welcomeimg = welcomepic(pic, user.first_name, member.chat.title, user.id, user.username, Thumbnail)
        await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption=f"""

ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {member.chat.title}

ɴᴀᴍᴇ - {user.mention}
ᴜꜱᴇʀ ɴᴀᴍᴇ - @{user.username}
ᴜꜱᴇʀ ɪᴅ  - {user.id}

""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("sᴜᴍᴍᴏɴ ᴍᴇ", url=f"https://t.me/{app.username}?startgroup=new")],
            ])
        )
    except Exception as e:
        print(str(e))

    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception as e:
        print(str(e))


