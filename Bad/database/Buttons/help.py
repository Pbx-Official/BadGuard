from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_GROUP
from Bad import app


def support_group_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="۞ group ۞",
                    url=SUPPORT_GROUP,
                ),
            ]
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="۞ back ۞", callback_data=f"settings_back_helper"
                ),
                InlineKeyboardButton(text="۞ close ۞", callback_data=f"close"),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="۞ 𝐇𝙴𝙻𝙿 ۞", url=f"https://t.me/{app.username}?start=help"
            )
        ],
    ]
    return buttons

# ---- ADD THIS FUNCTION ----
def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="💠 𝐀𝙳𝙳 𝙼𝙴 𝙸𝙽 𝙽𝙴𝚆 𝙶𝚁𝙾𝚄𝙿𝚂 💠",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text="۞ 𝐇𝙴𝙻𝙿 ۞", callback_data="settings_back_helper"),
            InlineKeyboardButton(text="☢ 𝐒𝙴𝚃 ☢", callback_data="settings_helper"),
        ],
        [
            InlineKeyboardButton(text="✡ 𝐆𝚁𝙾𝚄𝙿 ✡", url=SUPPORT_GROUP),
        ],
    ]
    return buttons

def close_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ]
        ]
    )
    return upl
