import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from Bad import app

@app.on_message(filters.command(["mmf", "memify"]))
async def memify(_, message: Message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message

    if not reply_message:
        await message.reply_text("**Reply to an sticker to memify it.**")
        return

    if len(message.text.split()) < 2:
        await message.reply_text("**Give me text after /mmf to memify.**")
        return

    msg = await message.reply_text("**Memifying this image!**")
    text = message.text.split(None, 1)[1]
    file = await app.download_media(reply_message)

    meme = await drawText(file, text)
    await app.send_document(chat_id, document=meme)

    await msg.delete()

    if os.path.exists(meme):
        os.remove(meme)

async def drawText(image_path, text):
    img = Image.open(image_path)

    if os.path.exists(image_path):
        os.remove(image_path)

    i_width, i_height = img.size

    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "./resources/fonts/default.ttf"

    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    draw = ImageDraw.Draw(img)

    current_h, pad = 10, 5

    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)

            draw.text(
                xy=(((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)

            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    image_name = "memify.webp"
    webp_file = os.path.join(image_name)

    img.save(webp_file, "webp")

    return webp_file


__MODULE__ = "ᴍᴇᴍɪꜰʏ"
__HELP__ = """ 

## ᴍᴇᴍɪꜰʏ 📝

» `/mmf <text>` : 
ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ꜱᴛɪᴄᴋᴇʀ ᴀɴᴅ ᴀᴅᴅ ᴀ ᴛᴇxᴛ ᴏɴ ɪᴛ ʟɪᴋᴇ ᴀ ᴍᴇᴍᴇ  
ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴇᴅɪᴛꜱ ᴛʜᴇ ꜱᴛɪᴄᴋᴇʀ ɪɴᴛᴏ ᴀ ᴍᴇᴍᴇ ᴡɪᴛʜ ʏᴏᴜʀ ᴛᴇxᴛ 💬

"""
