import os 
import random
import asyncio
from PIL import Image, ImageDraw
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from Bad import app

from pyrogram.enums import ChatAction, ChatType
from typing import Dict, Union
from pymongo import MongoClient
from config import MONGO_DB_URI, DB_NAME
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

client = MongoClient(MONGO_DB_URI)
db = client[DB_NAME]

coupledb = db.couple
karmadb = db.karma

async def get_image(cid: int):
    chat_data = coupledb.get(cid, {})
    image = chat_data.get("img", "")
    return image

async def _get_lovers(chat_id: int):
    lovers = coupledb.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers

async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False

async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    coupledb.update_one({"chat_id": chat_id}, {"$set": {"couple": lovers}}, upsert=True)

async def select_couples(chat_id: int):
    list_of_users = []
    async for i in app.get_chat_members(chat_id, limit=50):
        if not i.user.is_bot:
            list_of_users.append(i.user.id)
    
    c1_id = random.choice(list_of_users)
    c2_id = random.choice(list_of_users)
    while c1_id == c2_id:
        c1_id = random.choice(list_of_users)
    
    N1 = (await app.get_users(c1_id)).mention
    N2 = (await app.get_users(c2_id)).mention

    couple = {
        "c1_id": c1_id,
        "c2_id": c2_id,
        "N1": N1,
        "N2": N2
    }
    return couple

@app.on_message(
    filters.command(["couples", "couple", "shipping"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
)
async def couples(app, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")
    
    # Send loading emoji
    loading_message = await message.reply_text("❤️")

    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    couple = await get_couple(cid, current_date)
    
    if not couple:
        couple = await select_couples(cid)
        await save_couple(cid, current_date, couple)
    
    c1_id = couple["c1_id"]
    c2_id = couple["c2_id"]
    N1 = couple["N1"]
    N2 = couple["N2"]
    
    photo1 = (await app.get_chat(c1_id)).photo
    photo2 = (await app.get_chat(c2_id)).photo

    try:
        p1 = await app.download_media(photo1.big_file_id, file_name="pfp.png")
    except Exception:
        p1 = "resources/image/C/coupless.png"
    try:
        p2 = await app.download_media(photo2.big_file_id, file_name="pfp1.png")
    except Exception:
        p2 = "resources/image/C/coupless.png"

    img1 = Image.open(f"{p1}")
    img2 = Image.open(f"{p2}")
    xy = ["Zero1", "Zero2", "Zero3"]
    x = random.choice(xy)

    img = Image.open(f"resources/image/C/{x}.png")

    img1 = img1.resize((680, 680))
    img2 = img2.resize((680, 680))

    mask = Image.new('L', img1.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img1.size, fill=255)

    mask1 = Image.new('L', img2.size, 0)
    draw = ImageDraw.Draw(mask1)
    draw.ellipse((0, 0) + img2.size, fill=255)

    img1.putalpha(mask)
    img2.putalpha(mask1)

    draw = ImageDraw.Draw(img)

    img.paste(img1, (185, 359), img1)
    img.paste(img2, (1696, 359), img2)

    img.save(f'test_{cid}.png')

    next_date = (datetime.utcnow() + timedelta(days=1)).strftime("%d/%m/%Y 12 AM")

    TXT = f"""
✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴅᴀʏ ✧
❍═══════════════════❍
{N1} + {N2} = ❣️
❍═══════════════════❍
ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ {next_date}
    """
    await app.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    await message.reply_photo(f"test_{cid}.png", caption=TXT)
    await loading_message.delete()
    
    try:
        os.remove(f"./downloads/pfp1.png")
        os.remove(f"./downloads/pfp2.png")
        os.remove(f"test_{cid}.png")
    except Exception:
        pass

@app.on_callback_query(filters.regex("coupless"))
async def regeneratecouples(client: Client, cb: CallbackQuery):
    uid = cb.from_user.id
    chat = cb.message.chat
    xyz = cb.from_user.mention
    list_of_users = []
    
    if uid in Owner:
        pass
    else:
        member = await chat.get_member(uid)
        if member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
            pass
        else:
            await cb.answer("ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ !", show_alert=True)

    async for i in app.get_chat_members(cb.message.chat.id, limit=90):
        if not i.user.is_bot:
            list_of_users.append(i.user.id)

    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    couple = await select_couples(cb.message.chat.id)
    await save_couple(cb.message.chat.id, current_date, couple)

    c1_id = couple["c1_id"]
    c2_id = couple["c2_id"]
    N1 = couple["N1"]
    N2 = couple["N2"]

    photo1 = (await app.get_chat(c1_id)).photo
    photo2 = (await app.get_chat(c2_id)).photo

    try:
        p1 = await app.download_media(photo1.big_file_id, file_name="pfp.png")
    except Exception:
        p1 = "resources/image/C/coupless.png"
    try:
        p2 = await app.download_media(photo2.big_file_id, file_name="pfp1.png")
    except Exception:
        p2 = "resources/image/C/coupless.png"

    img1 = Image.open(p1)
    img2 = Image.open(p2)
    xy = ["Zero1", "Zero2", "Zero3"]
    x = random.choice(xy)

    img = Image.open(f"resources/image/C/{x}.png")

    img1 = img1.resize((680, 680))
    img2 = img2.resize((680, 680))

    mask = Image.new('L', img1.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img1.size, fill=255)

    mask1 = Image.new('L', img2.size, 0)
    draw = ImageDraw.Draw(mask1)
    draw.ellipse((0, 0) + img2.size, fill=255)

    img1.putalpha(mask)
    img2.putalpha(mask1)

    draw = ImageDraw.Draw(img)

    img.paste(img1, (185, 359), img1)
    img.paste(img2, (1696, 359), img2)

    cid = cb.message.chat.id
    img.save(f'test_{cid}.png')

    next_date = (datetime.utcnow() + timedelta(days=1)).strftime("%d/%m/%Y 12 AM")

    TXT = f"""
✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴅᴀʏ ✧
❍═══════════════════❍
{N1} + {N2} = ❣️
❍═══════════════════❍
ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ {next_date}
    """
    await app.send_chat_action(cid, ChatAction.UPLOAD_PHOTO)
    await cb.message.reply_photo(f"test_{cid}.png", caption=TXT)

    try:
        os.remove("pfp.png")
        os.remove("pfp1.png")
        os.remove(f"test_{cid}.png")
    except Exception:
        pass

__MODULE__ = "ᴄᴏᴜᴘʟᴇ"
__HELP__ = """ 

## ᴄᴏᴜᴘʟᴇ 👩‍❤️‍👨
**ᴏɴʟʏ ꜰᴏʀ ɢʀᴏᴜᴘꜱ**

» `/couple` : ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴄᴏᴜᴘʟᴇ ᴘᴀɪʀꜱ ꜰʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴄᴜᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟꜱ 🎈

"""
