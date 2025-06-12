import random
from pyrogram import Client, filters
from pyrogram.emoji import *
import pyrogram 

from Bad import app 


@app.on_message(filters.command("emoji"))
async def random_emoji(client, message):
    random_emoji = random.choice(list(vars(pyrogram.emoji).values()))

    await message.reply_text(random_emoji)

