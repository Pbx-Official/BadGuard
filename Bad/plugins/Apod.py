from pyrogram import Client, filters
import requests

from Bad import app

@app.on_message(filters.command("apod"))
async def shalini(client, message):
    
    api_url = "https://themagixapi.onrender.com/space/apod"
    
    try:
    
        response = requests.get(api_url)
        response.raise_for_status() 
        data = response.json()

 
        title = data.get("title", "No Title")
        date = data.get("date", "No Date")
        description = data.get("description", "No Description")
        image_url = data.get("imageUrl", None)

   
        if image_url:
            caption = f"**{title}**\n\n📅 Date: {date}\n\n{description}"
            await message.reply_photo(photo=image_url, caption=caption)
        else:
            await message.reply_text("No image available for today.")

    except requests.RequestException as e:
        await message.reply_text(f"Failed to fetch APOD: {e}")
