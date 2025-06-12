from pyrogram import Client, filters
import requests, random 
from pyrogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto)
from Bad import app
import nekos
from config import Zero, MARIN, RANDOMIMG

@app.on_message(filters.command(["pfp", "animepfp"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def animeimages(client, message):
    await message.reply_photo(
        photo="https://telegra.ph/file/00734ac3f3ebfe9cb264f.jpg",
        caption="ᴄʜᴏᴏsᴇ ᴡʜɪᴄʜ ᴛʏᴘᴇ ᴘғᴘ ʏᴏᴜ ᴡᴀɴᴛ :",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="ᴢᴇʀᴏ ᴛᴡᴏ", callback_data="zerotwoo"),
                    InlineKeyboardButton(text="ᴍᴀʀɪɴ ᴋɪᴛᴀɢᴀᴠᴀ ", callback_data="marinkitagava"),
                ],
                [
                    InlineKeyboardButton(text="ɴᴇᴋᴏ ᴀɴɪᴍᴇ [ V1 ]", callback_data="animev1"),
                    InlineKeyboardButton(text="ɴᴇᴋᴏ ᴀɴɪᴍᴇ [ V2 ]", callback_data="animev2"),
                ],
                [
                    InlineKeyboardButton(text="ɴᴇᴋᴏ ᴀɴɪᴍᴇ [ᴠ𝟹]", callback_data="nekov3"),
                    InlineKeyboardButton(text="ɴᴇᴋᴏ ᴀɴɪᴍᴇ [ᴠ4]", callback_data="nekov4"),
                ],
                [
                    InlineKeyboardButton(text="ʜᴜꜱʙᴀɴᴅᴏ", callback_data="animeboyspfp"),
                    InlineKeyboardButton(text="ғᴏx ɢɪʀʟ", callback_data="foxgirlz"),
                ],
                [
                    InlineKeyboardButton(text="ᴋɪᴛsᴜɴᴇ", callback_data="kitsunepfp"),
                    InlineKeyboardButton(text="Wᴀɪғᴜ", callback_data="waifupfp"),
                ],
                [
                    InlineKeyboardButton(text="ʀᴀɴᴅᴏᴍ ɪᴍᴀɢᴇꜱ", callback_data="randomimgs"),
                ],
            ]
        )
    )


@app.on_callback_query(filters.regex("animev1"))
async def animev1callback(client, cb: CallbackQuery):
    response = requests.get("https://api.waifu.pics/sfw/neko").json()
    try:
        up = response['url']
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="animev1")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(up),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("animev2"))
async def animev2callback(client, cb: CallbackQuery):
    response = requests.get("https://nekos.best/api/v2/neko").json()
    try:
        image_url = response["results"][0]["url"]
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="animev2")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(image_url),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("animeboyspfp"))
async def animeboyspfp(client, cb: CallbackQuery):
    response = requests.get("https://nekos.best/api/v2/husbando").json()
    try:
        image_url = response["results"][0]["url"]
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="animeboyspfp")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(image_url),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("kitsunepfp"))
async def kitsunepfp(client, cb: CallbackQuery):
    response = requests.get("https://nekos.best/api/v2/kitsune").json()
    try:
        image_url = response["results"][0]["url"]
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="kitsunepfp")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(image_url),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass 


@app.on_callback_query(filters.regex("waifupfp"))
async def waifupfp(client, cb: CallbackQuery):
    response = requests.get("https://api.waifu.pics/sfw/waifu").json()
    try:
        image_url = response['url']
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="waifupfp")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(image_url),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("foxgirlz"))
async def foxgirlcallback(client, cb: CallbackQuery):
    try:
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="foxgirlz")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(nekos.img("fox_girl")),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("nekov3"))
async def nekov3callback(client, cb: CallbackQuery):
    try:
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="nekov3")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(nekos.img("neko")),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("nekov4"))
async def nekov4callback(client, cb: CallbackQuery):
    response = requests.get("https://nekos.life/api/v2/img/neko")
    data = response.json()
    neko_image_url = data["url"]
    try:
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="nekov4")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(neko_image_url),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass

@app.on_callback_query(filters.regex("zerotwoo"))
async def nekov4callback(client, cb: CallbackQuery):
    try:
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="zerotwoo")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(random.choice(Zero)),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("marinkitagava"))
async def nekov4callback(client, cb: CallbackQuery):
    try:
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="marinkitagava")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(random.choice(MARIN)),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("randomimgs"))
async def nekov4callback(client, cb: CallbackQuery):
    try:
        buttons = [
            [InlineKeyboardButton("ɢᴇɴᴇʀᴀᴛᴇ ᴀɢᴀɪɴ ", callback_data="randomimgs")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="animemain"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
        ]
        await cb.message.edit_media(
            media=InputMediaPhoto(random.choice(RANDOMIMG)),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        pass


@app.on_callback_query(filters.regex("animemain"))
async def animemain(client, cb: CallbackQuery):
    try:
        await cb.message.edit_media(
            media=InputMediaPhoto("https://telegra.ph/file/00734ac3f3ebfe9cb264f.jpg"),
        )
        await cb.message.edit_caption(
            caption="ᴄʜᴏᴏsᴇ ᴡʜɪᴄʜ ᴛʏᴘᴇ ᴘғᴘ ʏᴏᴜ ᴡᴀɴᴛ :",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton(text="ᴢᴇʀᴏ ᴛᴡᴏ", callback_data="zerotwoo"),
                    InlineKeyboardButton(text="ᴍᴀʀɪɴ ᴋɪᴛᴀɢᴀᴠᴀ ", callback_data="marinkitagava"),
                   ],
                    [
                        InlineKeyboardButton(text="ɴᴇᴋᴏ ᴀɴɪᴍᴇ [ V1 ]", callback_data="animev1"),
                        InlineKeyboardButton(text="ɴᴇᴋᴏ ᴀɴɪᴍᴇ [ V2 ]", callback_data="animev2"),
                    ],
                    [
                        InlineKeyboardButton(text="ɴᴇᴋᴏ ᴀɴɪᴍᴇ [ᴠ𝟹]", callback_data="nekov3"),
                        InlineKeyboardButton(text="ɴᴇᴋᴏ ᴀɴɪᴍᴇ [ᴠ4]", callback_data="nekov4"),
                    ],
                    [
                        InlineKeyboardButton(text="ʜᴜꜱʙᴀɴᴅᴏ", callback_data="animeboyspfp"),
                        InlineKeyboardButton(text="ғᴏx ɢɪʀʟ", callback_data="foxgirlz"),
                    ],
                    [
                        InlineKeyboardButton(text="ᴋɪᴛsᴜɴᴇ", callback_data="kitsunepfp"),
                        InlineKeyboardButton(text="Wᴀɪғᴜ", callback_data="waifupfp"),
                    ],
                    [
                    InlineKeyboardButton(text="ʀᴀɴᴅᴏᴍ ɪᴍᴀɢᴇꜱ", callback_data="randomimgs"),
                    ],
                ]
            )
        )
    except Exception as e:
        pass

