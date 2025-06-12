import os
from pyrogram import Client, filters
import requests
from Bad import app
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command(["ccgen","cc","gencc","gen"]))
async def ccgen(client, message):
    command_parts = message.text.split()
    
    if len(command_parts) != 3:
        await message.reply_text(f"<u>ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ɪɴ ᴛʜɪꜱ ꜰᴏʀᴍᴀᴛ</u>\n\n/ccgen <YourBin> <How Much Cc U want> \n\n<u>**ᴇxᴀᴍᴘʟᴇ**</u>\n`/ccGen 327028 30`")
        return
    
    number, limit = command_parts[1], command_parts[2]
    url = f"https://api.safone.dev/ccgen?bins={number}&limit={limit}"
    regenerate_button = InlineKeyboardButton(
            "ʀᴇɢᴇɴᴇʀᴀᴛᴇ", callback_data=f"regenerate_{number}_{limit}"
        )
    keyboard = InlineKeyboardMarkup([[regenerate_button]])
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        if "liveCC" in data:
            cc_list = data["liveCC"]
            formatted_ccs = "\n".join(f"{cc}" for cc in cc_list)
            
            if len(formatted_ccs) <= 4096:  # Tg msg lenth 
                await message.reply_text(f"<u>ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʟɪᴠᴇ ᴄʀᴇᴅɪᴛ ᴄᴀʀᴅꜱ </u> \n\n{formatted_ccs}", reply_markup=keyboard)
            else:
                file_path = "shivaniccs.txt"
                with open(file_path, "w") as file:
                    file.write(formatted_ccs)
                
                await message.reply_document(file_path, caption=f"ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʟɪᴠᴇ ᴄʀᴇᴅɪᴛ ᴄᴀʀᴅꜱ  \n\n||ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ {app.mention}||")
                os.remove(file_path)
        else:
            await message.reply_text("ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ ...")
            
    except requests.RequestException as e:
        await message.reply_text(f"Error: {e}")



@app.on_callback_query(filters.regex(r"regenerate_"))
async def regenerate_cc(client, callback_query):
    number = callback_query.data.split("_")[1]
    limit = callback_query.data.split("_")[2]
    url = f"https://api.safone.dev/ccgen?bins={number}&limit={limit}"
    regenerate_button = InlineKeyboardButton(
            "ʀᴇɢᴇɴᴇʀᴀᴛᴇ", callback_data=f"regenerate_{number}_{limit}"
        )
    keyboard = InlineKeyboardMarkup([[regenerate_button]])
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        await client.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
        if "liveCC" in data:
            cc_list = data["liveCC"]
            formatted_ccs = "\n".join(f"{cc}" for cc in cc_list)
            await callback_query.edit_message_text(f"<u>ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʟɪᴠᴇ ᴄʀᴇᴅɪᴛ ᴄᴀʀᴅꜱ </u> \n\n{formatted_ccs}", reply_markup=keyboard)
        else:
            await callback_query.message.reply_text("ꜱᴇʀᴠᴇʀ ɪꜱꜱᴜᴇꜱ ...")
            
    except requests.RequestException as e:
        await callback_query.message.reply_text(f"Error: {e}")
        
           
