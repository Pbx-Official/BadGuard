from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from googlesearch import search
from Bad import app


@app.on_message(filters.command(["google"]))
async def google(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("**Example:**\n\n`/google who is zero two`")
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])
    xy = await message.reply_text("**Sᴇᴀʀᴄʜɪɴɢ ᴏɴ Gᴏᴏɢʟᴇ....**")
    try:
        s = search(user_input, advanced=True)
        txt = f"Search Query: {user_input}\n\nresults"
        for result in s:
            txt += f"\n\n[❍ {result.title}]({result.url})\n<b>{result.description}</b>"
        await xy.edit(
            txt,
            disable_web_page_preview=True,
        )
    except Exception as e:
        print(e)


__MODULE__ = "ɢᴏᴏɢʟᴇ"
__HELP__ = """ 

## ɢᴏᴏɢʟᴇ 🌐

» `/google <query>` : ꜱᴇᴀʀᴄʜ ᴀɴʏᴛʜɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ɢᴇᴛ ɪɴꜱᴛᴀɴᴛ ʀᴇꜱᴜʟᴛꜱ

"""
