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
