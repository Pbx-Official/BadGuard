from pyrogram.types import InlineKeyboardButton

import config
from Bad import app



start_pannel()
    buttons = [
        [
            InlineKeyboardButton(
                text="۞ 𝐇𝙴𝙻𝙿 ۞", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text="۞ 𝐇𝙴𝙻𝙿 ۞", url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


private_panel()
    buttons = [
        [
            InlineKeyboardButton(
                text="۞ 𝐇𝙴𝙻𝙿 ۞",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text="۞ 𝐇𝙴𝙻𝙿 ۞", user_id=config.OWNER_ID),
            InlineKeyboardButton(text="۞ 𝐇𝙴𝙻𝙿 ۞", url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text="۞ 𝐇𝙴𝙻𝙿 ۞", url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton(text="۞ 𝐇𝙴𝙻𝙿 ۞", url=config.UPSTREAM_REPO),
        ],
        [InlineKeyboardButton(text="۞ 𝐇𝙴𝙻𝙿 ۞", callback_data="settings_back_helper")],
    ]
    return buttons

def alive_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="✿︎ ᴀᴅᴅ ᴍᴇ ✿︎", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
        ],
    ]
    return buttons
