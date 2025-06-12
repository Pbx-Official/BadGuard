import requests 
from pyrogram import Client, filters
from Bad import app


@app.on_message(filters.command(["bin", "ccbin", "bininfo"], [".", "!", "/"]))
async def check_ccbin(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "ɢɪᴠᴇ ᴍᴇ ᴀ ʙɪɴ ᴛᴏ ɢᴇᴛ ᴅᴇᴛᴀɪʟꜱ  !"
        )
    
    bin_number = message.command[1]
    response = requests.get(f"https://api.safone.dev/bininfo?bin={bin_number}")
    resp = response.json()
    if len(bin_number) < 6:
        return await aux.edit("ᴛʜᴇ ʙɪɴ ʏᴏᴜ ᴘʀᴏᴠɪᴅᴇᴅ ɪꜱ ᴡʀᴏɴɢ ")
    try:
        await message.reply_text(
        f"🏦 ʙᴀɴᴋ ➪ {resp['bank']}\n"
        f"💳 ʙɪɴ ➪ {resp['bin']}\n"
        f"🏡 ᴄɴ ➪ {resp['country']}\n"
        f"🇮🇳 ғʟᴀɢ ➪ {resp['flag']}\n"
        f"🧿 ɪsᴏ ➪ {resp['iso']}\n"
        f"⏳ ʟᴇᴠᴇʟ ➪ {resp['level']}\n"
        f"🔴 ᴘʀᴇᴘᴀɪᴅ ➪ {str(resp['prepaid'])}${'' if not resp['prepaid'] else '*Yes*'}\n"
        f"🆔 ᴛʏᴘᴇ ➪ {resp['type'].capitalize()}\n"
        f"ℹ️ ᴠᴇɴᴅᴏʀ ➪ {resp['vendor']}",
        
        
    )
    except:
        return await message.reply_text(f"""
ᴛʜᴇ ʙɪɴ ʏᴏᴜ ᴘʀᴏᴠɪᴅᴇᴅ ɪꜱ ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ʙɪɴ...""")
