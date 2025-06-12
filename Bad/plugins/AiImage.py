from pyrogram import Client, filters
import base64
import requests
import io, os
from config import LOG_GROUP_ID, OWNER_ID
from Bad import app 
import random 
import time
import json
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

API = [
    "5198e8e03dmsh8964c5e124e2423p1465fcjsn24fee55d765b",
    "0ebcdc50dbmshe65ff123652b7b4p1c40d9jsn4ab1f1712db4",
    "6cc113b9f1msh1f244a6defb90dep1b6531jsn4c0e887cd642",
    "eacee98f87msh41aee31eb23ba55p1490f2jsn2121da163166",
    "0f49257511mshf15d0a693448b21p139a7cjsna7fc4fcdf307",
    "ec29045c74mshd5bd965c6c9e063p18719djsn97b6e224cf92",
    "6abf3cae92msh2baa3aac2ed1b56p1d276ejsne4f75a9afb3d",
    "d95a67dfddmsh71a7421e9a5a26dp170571jsn59930db0013d",
    "c211e9f49dmshd6b2b7c73a126a4p1cbffajsndbd7e05975d6",
    "2aa80696b0mshd6c0ad0df2a015ep15b691jsnc97f5740422f",
]

url = "https://chatgpt-42.p.rapidapi.com/texttoimage"
headers = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": random.choice(API),
    "X-RapidAPI-Host": "chatgpt-42.p.rapidapi.com"
}

def send_query_to_api(query):
    payload = {
        "text": query
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get('generated_image', '')

@app.on_message(filters.command(["ImageGen", "imggen", "genimage"]))
async def genimg_command_handler(bot, message):
    try:
        query = " ".join(message.command[1:])

        if not query:
            await message.reply_text("ɢɪᴠᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀɴ ᴀɪ ʙᴀsᴇᴅ ɪᴍᴀɢᴇ (Normal)")
            return
        await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        msg = await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ 20 ꜱᴇᴄᴏɴᴅꜱ...❣️")
        generated_image_url = send_query_to_api(query)
        image_response = requests.get(generated_image_url)
        if image_response.status_code == 200:
            image_stream = io.BytesIO(image_response.content)

            await message.reply_photo(
                image_stream, 
                caption=f"ɪᴍᴀɢᴇ ɪs ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ {message.from_user.mention}\n\n||ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ {app.mention} ||", 
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(f"ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ", url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users")]
                    ]
                )
            )
            await msg.delete()
        else:
            await message.reply_text("ᴏʜ ꜱᴏʀʀʏ ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ \n\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ɪᴍᴀɢᴇ ᴛᴏᴏʟꜱ \n/start ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ...")
    except Exception as e:
        await message.reply_text("ᴏʜ ꜱᴏʀʀʏ ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ \n\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ɪᴍᴀɢᴇ ᴛᴏᴏʟꜱ \n/start ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ...")
        await app.send_message(LOG_GROUP_ID, f"An error occurred in Image generation (normal) \n**Error:** {e}")




def generate_images(prompt):
    url = base64.b64decode('aHR0cHM6Ly9haS1hcGkubWFnaWNzdHVkaW8uY29tL2FwaS9haS1hcnQtZ2VuZXJhdG9y').decode("utf-8")

    form_data = {
        'prompt': prompt,
        'output_format': 'bytes',
        'request_timestamp': str(int(time.time())),
        'user_is_subscribed': 'false',
    }

    response = requests.post(url, data=form_data)
    if response.status_code == 200:
        if response.content:
            return response.content
        else:
            raise Exception("ᴏʜ ꜱᴏʀʀʏ ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ \n\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ɪᴍᴀɢᴇ ᴛᴏᴏʟꜱ \n/start ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ...")
    else:
        raise Exception(f"ᴏʜ ꜱᴏʀʀʏ ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ \n\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ɪᴍᴀɢᴇ ᴛᴏᴏʟꜱ \n/start ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ...")

@app.on_message(filters.command("gencimg"))
async def generate_image_command(client: Client, message: Message):
    try:
        prompt = message.text.split(maxsplit=1)[1]
    except IndexError:
        await message.reply_text("ɢɪᴠᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀɴ ᴀɪ ʙᴀsᴇᴅ ɪᴍᴀɢᴇ (Cartoon).")
        return
    id = message.from_user.id
    msg = await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ 20 ꜱᴇᴄᴏɴᴅꜱ...❣️")
    try:
        image_data = generate_images(prompt)
       
        shivani = f"shivaniaigen{id}.jpg"
        with open(shivani, 'wb') as f:
            f.write(image_data)
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        await message.reply_photo(shivani, caption=f"<u>**ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ ɪᴍᴀɢᴇ**</u>\n\nʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ {message.from_user.mention} ")
        os.remove(shivani)   
        await msg.delete()
    except Exception as e:
        await message.reply_text("ᴏʜ ꜱᴏʀʀʏ ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ \n\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ɪᴍᴀɢᴇ ᴛᴏᴏʟꜱ \n/start ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ...")
        await app.send_message(LOG_GROUP_ID, f"An error occurred in Image generation (cartoon) \n**Error:** {e}")





def fetch_image(prompt):
    prompt_encoded = prompt.replace(" ", "%20")
    url = f"https://nandha-api.onrender.com/imagine?prompt={prompt_encoded}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"ᴏʜ ꜱᴏʀʀʏ ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ \n\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ɪᴍᴀɢᴇ ᴛᴏᴏʟꜱ \n/start ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ...")


@app.on_message(filters.command("genrimg"))
async def generate_image_command(client: Client, message: Message):
    id = message.from_user.id

    try:
        prompt = message.text.split(maxsplit=1)[1]
    except IndexError:
        await message.reply_text("ɢɪᴠᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀɴ ᴀɪ ʙᴀsᴇᴅ ɪᴍᴀɢᴇ (Realistic).")
        return
    msg = await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ 20 ꜱᴇᴄᴏɴᴅꜱ...❣️")

    try:
        image_data = fetch_image(prompt)
        
        image_path = f"shivani_{id}_R.jpg"
        with open(image_path, 'wb') as f:
            f.write(image_data)
            
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        
        await message.reply_photo(image_path, caption=f"<u>**ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ ɪᴍᴀɢᴇ**</u>\n\nʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ {message.from_user.mention} ")
        await msg.delete()
        os.remove(image_path)
    except Exception as e:
        await message.reply_text("ᴏʜ ꜱᴏʀʀʏ ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ \n\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ɪᴍᴀɢᴇ ᴛᴏᴏʟꜱ \n/start ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ...")
        await app.send_message(LOG_GROUP_ID, f"An error occurred in Image generation (realistic) \n**Error:** {e}")
