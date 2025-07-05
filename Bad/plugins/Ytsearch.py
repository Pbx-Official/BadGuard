import logging
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from Bad import app
from pyrogram import filters

@app.on_message(filters.command(["search", "ytsearch"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("/ytsearch needs an argument!")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text(" searching")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"Judul: {results[i]['title']}\n"
            text += f"Durasi: {results[i]['duration']}\n"
            text += f"Views: {results[i]['views']}\n"
            text += f"Channel: {results[i]['channel']}\n"
            text += f"https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))


__MODULE__ = "ʏᴛ ꜱᴇᴀʀᴄʜ"
__HELP__ = """

## ʏᴏᴜᴛᴜʙᴇ ꜱᴇᴀʀᴄʜ 🔎

» `/ytsearch <query>` : ꜱᴇᴀʀᴄʜ ᴀɴʏᴛʜɪɴɢ ᴏɴ ʏᴏᴜᴛᴜʙᴇ ᴀɴᴅ ɢᴇᴛ ᴛᴏᴘ ʀᴇꜱᴜʟᴛꜱ.

❖ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡɪʟʟ ꜰᴇᴛᴄʜ ᴛɪᴛʟᴇ, ᴛʜᴜᴍʙɴᴀɪʟ, ᴀɴᴅ ʟɪɴᴋꜱ ᴏꜰ ᴛᴏᴘ ᴠɪᴅᴇᴏꜱ.
"""
