import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

Owner = list(map(int, getenv("Owner", "7588172591").split()))



def small_caps(text):
    small_caps_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyz",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    )
    return text.translate(small_caps_map)
  
