from pyrogram import filters
from Bad.database.errordb import capture_err
from io import BytesIO
from aiohttp import ClientSession
from Bad import app

async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with ClientSession().post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image

@app.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            txt = message.reply_to_message.text
        else:
            return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    else:
        try:
            txt = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    m = await message.reply_text("ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴀʀʙᴏɴ...")
    carbon = await make_carbon(txt)
    await m.edit_text("ᴜᴩʟᴏᴀᴅɪɴɢ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴄᴀʀʙᴏɴ...")
    await app.send_photo(
        message.chat.id,
        photo=carbon,
        caption=f"» ʀᴇᴏ̨ᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}",
    )
    await m.delete()
    carbon.close()

__MODULE__ = "ᴄᴀʀʙᴏɴ"
__HELP__ = """ 

## ᴄᴀʀʙᴏɴ
» `/carbon` <text or reply> : ᴄʀᴇᴀᴛᴇ ᴀ ʙᴇᴀᴜᴛɪꜰᴜʟ ᴄᴀʀʙᴏɴ.ɴᴏᴡ ꜱɴɪᴘᴘᴇᴛ ꜰʀᴏᴍ ᴛᴇxᴛ

"""
