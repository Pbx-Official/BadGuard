from pyrogram import Client, filters
import requests
import base64
from io import BytesIO
from config import LOG_GROUP_ID
from Bad.misc import SUDOERS
from PIL import Image
from Bad import app
import os
from pyrogram.enums import ChatAction

@app.on_message(filters.command("ZGenerateAi"))
async def ggamkme(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide some text after the command.")
        return
    if message.from_user.id not in SUDOERS:
        await message.reply_text("Only For Sudoers")
        return

    text = message.text.split(" ", 1)[1]
    the_text = text.replace(" ", "%20")

    url = f"https://api.safone.dev/imagine/nsfw?prompt={the_text}&limit=1&model=CuteAnimation-10"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "image" in data and len(data["image"]) > 0:
            image_data = base64.b64decode(data["image"][0])
            image = BytesIO(image_data)
            await client.send_photo(
                chat_id=message.chat.id,
                photo=image,
                caption=f"Here is the image for: {text} \n\nGenerated By {app.mention}",
             #   protect_content=True
            )
        else:
            await message.reply_text("Server Issue Try again later")
    except Exception as e:
        await app.send_message(LOG_GROUP_ID, f"{e}")
        await message.reply_text("Server Issue Try again later")

@app.on_message(filters.command(["GenerateAi"]))
async def generate_image(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Please provide a text prompt.")
    
    if message.from_user.id not in SUDOERS:
        await message.reply_text("Only For Sudoers")
        return

    the_text = message.text.split(None, 1)[1].replace(" ", "%20")
    user_id = message.from_user.id
    url = f"https://api.safone.dev/imagine/nsfw?prompt={the_text}&limit=1&model=Animesh-21Pruned"

    msg = await message.reply_text("Processing your request...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        image_data = base64.b64decode(data['image'][0])
        image_path = f"{user_id}_Nsfw.jpg"
        with open(image_path, 'wb') as f:
            f.write(image_data)

        await app.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        await message.reply_photo(image_path, caption=f"<u>Successfully generated image</u>\n\nRequested by {message.from_user.mention}"
                                  #protect_content=True
                                 )
        await msg.delete()
        os.remove(image_path)
    except Exception as e:
        await app.send_message(LOG_GROUP_ID, f"An error occurred in nsfw generation \n\n{e}")
        await message.reply_text("Sorry, the server is currently unavailable. Please try again later.or try /ZGenerateAi")
        await msg.delete()

