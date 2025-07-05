from Bad import app
from config import OWNER_ID
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}
BOT_USERNAME = app.username

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Start Whisper", switch_inline_query_current_chat="")]])

async def _whisper(_, inline_query):
    data = inline_query.query
    results = []

    if len(data.split()) < 2:
        mm = [
            InlineQueryResultArticle(
                title="💒 Whisper",
                description=f"@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]",
                input_message_content=InputTextMessageContent(f"💒 Usage:\n\n@{BOT_USERNAME} [ USERNAME | ID ] [ TEXT ]"),
                thumb_url="https://telegra.ph/file/3cff0c7f998091b0cf4ee.jpg",
                reply_markup=switch_btn
            )
        ]
    else:
        try:
            user_id = data.split()[0]
            msg = data.split(None, 1)[1]
        except IndexError as e:
            pass

        try:
            user = await _.get_users(user_id)
        except:
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description="Invalid username or ID!",
                    input_message_content=InputTextMessageContent("Invalid username or ID!"),
                    thumb_url="https://telegra.ph/file/3cff0c7f998091b0cf4ee.jpg",
                    reply_markup=switch_btn
                )
            ]

        try:
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔩 One-Time Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description=f"Send a Whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"💒 You are sending a whisper to {user.first_name}.\n\nType your message/sentence."),
                    thumb_url="https://telegra.ph/file/3cff0c7f998091b0cf4ee.jpg",
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="🔩 One-Time Whisper",
                    description=f"Send a one-time whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"ᴀ ᴡʜɪsᴘᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ {user.first_name}.\n\nᴏɴʟʏ ʜᴇ / sʜᴇ ᴄᴀɴ ᴏᴘᴇɴ"),
                    thumb_url="https://telegra.ph/file/3cff0c7f998091b0cf4ee.jpg",
                    reply_markup=one_time_whisper_btn
                )
            ]
        except:
            pass

        try:
            whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
        except:
            pass

    results.append(mm)
    return results


@app.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id

    if user_id not in [from_user, to_user, OWNER_ID]:
        try:
            await _.send_message(from_user, f"{query.from_user.mention} is trying to open your whisper.")
        except Unauthorized:
            pass

        return await query.answer("This whisper is not for you 🚧", show_alert=True)

    search_msg = f"{from_user}_{to_user}"

    try:
        msg = whisper_db[search_msg]
    except:
        msg = "🚫 Error!\n\nWhisper has been deleted from the database!"

    SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("Go Inline 🪝", switch_inline_query_current_chat="")]])

    await query.answer(msg, show_alert=True)

    if len(data) > 3 and data[3] == "one":
        if user_id == to_user:
            await query.edit_message_text("📬 Whisper has been read!\n\nPress the button below to send a whisper!", reply_markup=SWITCH)


async def in_help():
    answers = [
        InlineQueryResultArticle(
            title="💒 Whisper",
            description=f"@{BOT_USERNAME} [USERNAME | ID] [TEXT]",
            input_message_content=InputTextMessageContent(f"**📍Usage:**\n\n@{app.username} (Target Username or ID) (Your Message).\n\n**Example:**\n@{app.username} @username Hello"),
            thumb_url="https://telegra.ph/file/3cff0c7f998091b0cf4ee.jpg",
            reply_markup=switch_btn
        )
    ]
    return answers


@app.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()

    if string.strip() == "":
        answers = await in_help()
        await inline_query.answer(answers)
    else:
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers[-1], cache_time=0)


__MODULE__ = "ᴡʜɪꜱᴘᴇʀ"
__HELP__ = """

## 💒 ᴡʜɪꜱᴘᴇʀ

» `@BrokenRobot_Bot <username|user_id> <text>` : ꜱᴇɴᴅ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴡʜɪꜱᴘᴇʀ ᴛᴏ ᴀɴʏ ᴜꜱᴇʀ ᴠɪᴀ ɪɴʟɪɴᴇ ᴍᴏᴅᴇ.
» ꜱᴜᴘᴘᴏʀᴛꜱ ʙᴏᴛʜ **ɴᴏʀᴍᴀʟ** ᴀɴᴅ **ᴏɴᴇ-ᴛɪᴍᴇ** ᴡʜɪꜱᴘᴇʀꜱ.

❖ ᴇxᴀᴍᴘʟᴇ:
`@BrokenRobot_Bot @PB_SUKH Hello!`

❖ ᴏɴᴇ-ᴛɪᴍᴇ ᴡʜɪꜱᴘᴇʀ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ʀᴇᴀᴅ ᴏɴᴄᴇ ʙʏ ᴛʜᴇ ʀᴇᴄɪᴘɪᴇɴᴛ.

"""
