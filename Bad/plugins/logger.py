from pyrogram import filters
from pyrogram.types import Message

from Bad import app
from Bad.misc import SUDOERS
from Bad.database.database import add_off, add_on

# Translation dictionary
_ = {
    "general_2": "❖ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ᴏᴜᴇʀʏ.\n\n● ᴇxᴄᴇᴘᴛɪᴏɴ ➥ <code>{0}</code>",
    "log_1": "<b>❖ ᴇxᴀᴍᴘʟᴇ ➥</b>\n● /logger [ᴏɴ | ᴏғғ]",
    "log_2": "❖ ᴇɴᴀʙʟᴇᴅ ʟᴏɢɢɪɴɢ.",
    "log_3": "❖ ᴅɪsᴀʙʟᴇᴅ ʟᴏɢɢɪɴɢ."
}

@app.on_message(filters.command(["logger"]) & SUDOERS)
async def logger(client, message: Message):
    try:
        usage = _["log_1"]
        if len(message.command) != 2:
            return await message.reply_text(usage)
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "enable":
            await add_on(2)
            await message.reply_text(_["log_2"])
        elif state == "disable":
            await add_off(2)
            await message.reply_text(_["log_3"])
        else:
            await message.reply_text(usage)
    except Exception as e:
        await message.reply_text(_["general_2"].format(str(e)))

__MODULE__ = "ʟᴏɢɢᴇʀ"
__HELP__ = """

## ʟᴏɢɢɪɴɢ 📓

» `/logger enable` : ᴇɴᴀʙʟᴇ ᴛʜᴇ ʟᴏɢɢɪɴɢ ꜱʏꜱᴛᴇᴍ.
» `/logger disable` : ᴅɪꜱᴀʙʟᴇ ᴛʜᴇ ʟᴏɢɢɪɴɢ ꜱʏꜱᴛᴇᴍ.

❖ ᴏɴʟʏ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.
"""
