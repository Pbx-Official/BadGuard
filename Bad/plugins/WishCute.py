from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
from Bad import app 


@app.on_message(filters.command("wish"))
async def wish(_, m):
    if len(m.command) < 2:
        await m.reply(" ᴀᴅᴅ ᴡɪꜱʜ ʙᴀʙʏ")
        return 

    api = requests.get("https://nekos.best/api/v2/happy").json()
    url = api["results"][0]['url']
    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)
    wish = f"๏ ʜᴇʏ {m.from_user.first_name}! "
    wish += f"๏ ʏᴏᴜʀ ᴡɪꜱʜ ➛ {text} "
    wish += f"๏ ᴘᴏꜱꜱɪʙʟᴇ ᴛᴏ ➛ {wish_count}%"

    await app.send_animation(
        chat_id=m.chat.id,
        animation=url,
        caption=wish,
        reply_markup=InlineKeyboardMarkup(
            [
              [
                InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users"),
              ]
            ]
        ),
    )

CUTIE = "https://telegra.ph/file/7f3f2e3a5f2978340c186.mp4"

@app.on_message(filters.command("cute"))
async def cute(_, message):
    if not message.reply_to_message:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
    else:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    CUTE = f"Ⰶ {mention} {mm}% ᴄᴜᴛᴇ ʙᴀʙʏ !"


    await app.send_video(
        chat_id=message.chat.id,
        video=CUTIE,
        caption=CUTE,
        reply_markup=InlineKeyboardMarkup(
            [
              [
                InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users"),
              ]
            ]
        ),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
    )
