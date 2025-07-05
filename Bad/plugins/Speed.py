import asyncio
import speedtest
from pyrogram import filters
from pyrogram.types import Message

from Bad import app
from Bad.misc import SUDOERS

_ = {
    "server_11": "❖ ʀᴜɴɴɪɴɢ ᴀ sᴘᴇᴇᴅᴛᴇsᴛ...",
    "server_12": "<b>❖ ʀᴜɴɴɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ sᴩᴇᴇᴅᴛᴇsᴛ...</b>",
    "server_13": "<b>❖ ʀᴜɴɴɪɴɢ ᴜᴩʟᴏᴀᴅ sᴩᴇᴇᴅᴛᴇsᴛ...</b>",
    "server_14": "<b>❖ sʜᴀʀɪɴɢ sᴩᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs...</b>",
    "server_15": (
        "❖ <b>sᴩᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs</b> ❖\n\n"
        "<b>● ᴄʟɪᴇɴᴛ ➥</b>\n"
        "<b>● ɪsᴩ ➥</b> {0}\n"
        "<b>● ᴄᴏᴜɴᴛʀʏ ➥</b> {1}\n\n"
        "<b>● sᴇʀᴠᴇʀ ➥</b>\n"
        "<b>● ɴᴀᴍᴇ ➥</b> {2}\n"
        "<b>● ᴄᴏᴜɴᴛʀʏ ➥ </b> {3}, {4}\n"
        "<b>● sᴩᴏɴsᴏʀ ➥</b> {5}\n"
        "<b>● ʟᴀᴛᴇɴᴄʏ ➥</b> {6}\n"
        "<b>● ᴩɪɴɢ ➥</b> {7}"
    )
}

async def speedtest_function(client, message: Message, _):
    m = await message.reply_text(_["server_11"])

    try:
        test = speedtest.Speedtest()
        test.get_best_server()

        await m.edit_text(_["server_12"])
        test.download()

        await m.edit_text(_["server_13"])
        test.upload()

        test.results.share()

        await m.edit_text(_["server_14"])
        result = test.results.dict()

        output = _["server_15"].format(
            result["client"]["isp"],
            result["client"]["country"],
            result["server"]["name"],
            result["server"]["country"],
            result["server"]["cc"],
            result["server"]["sponsor"],
            result["server"]["latency"],
            result["ping"],
        )

        await message.reply_photo(photo=result["share"], caption=output)
        await m.delete()

    except Exception as e:
        await m.edit_text(f"<code>{e}</code>")


__MODULE__ = "ꜱᴇʀᴠᴇʀ ꜱᴘᴇᴇᴅ"
__HELP__ = """
**<u>ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ⚡</u>**

» `/speedtest` - ᴄʜᴇᴄᴋ sᴇʀᴠᴇʀ'ꜱ ᴅᴏᴡɴʟᴏᴀᴅ, ᴜᴘʟᴏᴀᴅ sᴘᴇᴇᴅ, ʟᴀᴛᴇɴᴄʏ, ᴀɴᴅ ᴘɪɴɢ.
• ʀᴜɴꜱ ᴀ ꜰᴜʟʟ ꜱᴘᴇᴇᴅ ᴀɴᴀʟʏꜱɪꜱ ᴀɴᴅ ʀᴇᴛᴜʀɴꜱ ᴀ ꜱʜᴀʀᴇᴀʙʟᴇ ɪᴍᴀɢᴇ.
• ᴏɴʟʏ ᴀᴄᴄᴇꜱꜱɪʙʟᴇ ʙʏ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ.
"""
