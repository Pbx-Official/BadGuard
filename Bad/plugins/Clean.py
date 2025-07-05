import os
import shutil

from pyrogram import filters

from Bad import app
from Bad.misc import SUDOERS


@app.on_message(filters.command("clean") & SUDOERS)
async def clean(_, message):
    A = await message.reply_text("ᴄʟᴇᴀɴɪɴɢ ᴛᴇᴍᴘ ᴅɪʀᴇᴄᴛᴏʀɪᴇs...")
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await A.edit("ᴛᴇᴍᴘ ᴅɪʀᴇᴄᴛᴏʀɪᴇs ᴀʀᴇ ᴄʟᴇᴀɴᴇᴅ")
  

__MODULE__ = "ᴄʟᴇᴀɴᴇʀ"
__HELP__ = """

## ᴄʟᴇᴀɴᴇʀ 🧹

» `/clean` : ᴄʟᴇᴀɴ ᴛʜᴇ ᴛᴇᴍᴘ ᴅɪʀᴇᴄᴛᴏʀɪᴇꜱ (downloads & cache).

❖ ᴏɴʟʏ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.
"""
