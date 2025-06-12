from pyrogram.types import InputMediaPhoto, Message
import random
import json
import requests
from Bad import app
from bs4 import BeautifulSoup as BSP
from pyrogram import client, filters

def split_url(url):
    return url.split('&')[0]

def get_image_urls(search_query):
    url = f"https://cn.bing.com/images/search?q={search_query}&first=1&cw=1177&ch=678"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    rss = requests.get(url, headers=headers)
    soup = BSP(rss.content, "html.parser")

    all_img = []
    for img in soup.find_all('img'):
        img_url = img.get('src2')
        if img_url and img_url.startswith('https://tse2.mm.bing.net/'):
            img_url = split_url(img_url)
            all_img.append(img_url)

    return all_img

@app.on_message(
   filters.command(["image", "images"])
)
async def image_generator(client, message):
    try:
        image_name = " ".join(message.command[1:])
        if not image_name:
            await message.reply_text("ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀɴ ɪᴍᴀɢᴇ ɴᴀᴍᴇ ᴛᴏ sᴇᴀʀᴄʜ ɪᴛ.")
            return

        if len(image_name) > 180:
            await message.reply_text("sᴏʀʀʏ ᴛʜᴇ ᴛᴇxᴛ ʏᴏᴜ ᴘʀᴏᴠɪᴅᴇᴅ ɪs ᴛᴏᴏ ʟᴏɴɢ ᴘʟᴇᴀsᴇ ᴅᴏɴ'ᴛ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ")
            return

        image_urls = get_image_urls(image_name)
        a = await message.reply_text(f"sᴇᴀʀᴄʜɪɴɢ ɪᴍᴀɢᴇs...")

        # Prepare media group
        media = []
        count = 0
        for img_url in image_urls:
            if count == 9:
                break
            # Create InputMediaPhoto object for each image URL
            media.append(InputMediaPhoto(media=img_url))
            count += 1

        # Send the media group as a reply to the user
        await message.reply_media_group(media=media)
        await message.delete()
        await a.delete()

    except Exception as e:
        await message.reply_text(f"Error: {e}")



 # bing img 2 

@app.on_message(
   filters.command(["bingimg", "bingimage"])
)
async def bing_image(client, message):
    try:
        text = message.text.split(None, 1)[
            1
        ]  # Extract the query from command arguments
    except IndexError:
        return await message.reply_text(
            "ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴀ ǫᴜᴇʀʏ ᴛᴏ sᴇᴀʀᴄʜ!"
        )  # Return error if no query is provided

    search_message = await message.reply_text( f"🔎" )  # Display searching message

    # Send request to Bing image search API
    url = "https://sugoi-api.vercel.app/bingimg?keyword=" + text
    resp = requests.get(url)
    images = json.loads(resp.text)  # Parse the response JSON into a list of image URLs

    media = []
    count = 0
    for img in images:
        if count == 7:
            break

        # Create InputMediaPhoto object for each image URL
        media.append(InputMediaPhoto(media=img))
        count += 1

    # Send the media group as a reply to the user
    await message.reply_media_group(media=media)

    # Delete the searching message and the original command message
    await search_message.delete()
    await message.delete()


