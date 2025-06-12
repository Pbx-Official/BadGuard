from Bad import app
import asyncio
import requests
from pyrogram import client, filters
import nekos
from pyrogram.types import Message 



@app.on_message(filters.command("neko"))

async def nekoimgg(client, message):
  await message.reply_photo(nekos.img("neko"))

@app.on_message(filters.command("slap"))
async def slappp(client, message):
    try:
        if message.reply_to_message:
            await message.reply_video(nekos.img("slap"), caption=f"{message.from_user.mention} slapped {message.reply_to_message.from_user.mention}")
        else:
            await message.reply_video(nekos.img("slap"))
    except Exception as e:
        await message.reply_text(f"Error: {e}")


@app.on_message(filters.command("tickle"))
async def tickleee(client, message):
    try:
        if message.reply_to_message:
            await message.reply_video(nekos.img("tickle"), caption=f"{message.from_user.mention} tickle {message.reply_to_message.from_user.mention}")
        else:
            await message.reply_video(nekos.img("tickle"))
    except Exception as e:
        await message.reply_text(f"Error: {e}")


@app.on_message(filters.command("feed"))
async def feedd(client, message):
  await message.reply_video(nekos.img("feed"))

@app.on_message(filters.command("lizard"))
async def lizard(client, message):
  a = await message.reply_text(f"🦎")
  await asyncio.sleep(0.02)
  await message.reply_photo(nekos.img("lizard"))
  await a.delete()

@app.on_message(filters.command("pat"))
async def feedd(client, message):
  await message.reply_photo(nekos.img("pat"))



@app.on_message(filters.command("kiss"))
async def kisss(client, message):
    try:
        if message.reply_to_message:
            await message.reply_video(nekos.img("kiss"), caption=f"{message.from_user.mention} kissed {message.reply_to_message.from_user.mention} 👩‍❤️‍💋‍👨")
        else:
            await message.reply_video(nekos.img("kiss"))
    except Exception as e:
        await message.reply_text(f"Error: {e}")


@app.on_message(filters.command("hug"))
async def kisss(client, message):
    try:
        if message.reply_to_message:
            await message.reply_video(nekos.img("hug"), caption=f"{message.from_user.mention} hugged {message.reply_to_message.from_user.mention}")
        else:
            await message.reply_video(nekos.img("hug"))
    except Exception as e:
        await message.reply_text(f"Error: {e}")



@app.on_message(
    filters.command(
        [
            "dice",
            "ludo",
            "dart",
            "basket",
            "basketball",
            "football",
            "slot",
            "bowling",
            "jackpot",
        ]
    )
)
async def dice(c, m: Message):
    command = m.text.split()[0]
    if command == "/dice" or command == "/ludo":

        value = await c.send_dice(m.chat.id, reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))

    elif command == "/dart":

        value = await c.send_dice(m.chat.id, emoji="🎯", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))

    elif command == "/basket" or command == "/basketball":
        basket = await c.send_dice(m.chat.id, emoji="🏀", reply_to_message_id=m.id)
        await basket.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(basket.dice.value))

    elif command == "/football":
        value = await c.send_dice(m.chat.id, emoji="⚽", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))

    elif command == "/slot" or command == "/jackpot":
        value = await c.send_dice(m.chat.id, emoji="🎰", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))
    elif command == "/bowling":
        value = await c.send_dice(m.chat.id, emoji="🎳", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))


bored_api_url = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command("bored", prefixes="/"))
async def bored_command(client, message):
    response = requests.get(bored_api_url)
    if response.status_code == 200:
        data = response.json()
        activity = data.get("activity")
        if activity:
            await message.reply(f"𝗙𝗲𝗲𝗹𝗶𝗻𝗴 𝗯𝗼𝗿𝗲𝗱? 𝗛𝗼𝘄 𝗮𝗯𝗼𝘂𝘁:\n\n {activity}")
        else:
            await message.reply("Nᴏ ᴀᴄᴛɪᴠɪᴛʏ ғᴏᴜɴᴅ.")
    else:
        await message.reply("Fᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴀᴄᴛɪᴠɪᴛʏ.")
