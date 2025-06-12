import datetime
import html
import textwrap
import bs4
import jikanpy
from pyrogram.enums import ParseMode
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Bad import app


info_btn = "More Information"

prequel_btn = "⬅️ "
sequel_btn = "➡️"
close_btn = "Close"

def shorten(description, info="anilist.co"):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + "...."
        msg += f"\nᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ : {description} [ʀᴇᴀᴅ ᴍᴏʀᴇ]({info})"
    else:
        msg += f"\nᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ : {description}"
    return msg



def t(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Days, ") if days else "")
        + ((str(hours) + " Hours, ") if hours else "")
        + ((str(minutes) + " Minutes, ") if minutes else "")
        + ((str(seconds) + " Seconds, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]

airing_query = """
query ($id: Int,$search: String) { 
    Media (id: $id, type: ANIME,search: $search) {
        id
        episodes
        title {
            romaji
            english
            native
        }
        nextAiringEpisode {
            airingAt
            timeUntilAiring
            episode
        } 
    }
}
"""

fav_query = """
query ($id: Int) {
    Media (id: $id, type: ANIME) {
        id
        title {
            romaji
            english
            native
        }
    }
}
"""

anime_query = """
query ($id: Int,$search: String) {
    Media (id: $id, type: ANIME,search: $search) {
        id
        title {
            romaji
            english
            native
        }
        description (asHtml: false)
        startDate{
            year
        }
        episodes
        season
        type
        format
        status
        duration
        siteUrl
        studios{
            nodes{
                name
            }
        }
        trailer{
            id
            site
            thumbnail
        }
        averageScore
        genres
        bannerImage
    }
}
"""

character_query = """
query ($query: String) {
    Character (search: $query) {
        id
        name {
            first
            last
            full
        }
        siteUrl
        image {
            large
        }
        description
    }
}
"""

manga_query = """
query ($id: Int,$search: String) { 
    Media (id: $id, type: MANGA,search: $search) { 
        id
        title {
            romaji
            english
            native
        }
        description (asHtml: false)
        startDate{
            year
        }
        type
        format
        status
        siteUrl
        averageScore
        genres
        bannerImage
    }
}
"""

url = "https://graphql.anilist.co"

def extract_arg(message):
    split = message.text.split(" ", 1)
    if len(split) > 1:
        return split[1]
    reply = message.reply_to_message
    if reply is not None:
        return reply.text
    return None

@app.on_message(filters.command("airing"))
async def airing(client, message):
    search_str = extract_arg(message)
    if not search_str:
        await message.reply_text("Tell Anime Name :) ( /airing <anime name>)")
        return
    variables = {"search": search_str}
    response = requests.post(
        url, json={"query": airing_query, "variables": variables}
    ).json()["data"]["Media"]
    msg = f"Name: {response['title']['romaji']} ({response['title']['native']})\nID: {response['id']}"
    if response["nextAiringEpisode"]:
        time = response["nextAiringEpisode"]["timeUntilAiring"] * 1000
        time = t(time)
        msg += f"\nEpisode: {response['nextAiringEpisode']['episode']}\nAiring In: {time}"
    else:
        msg += f"\nEpisode: {response['episodes']}\nStatus: N/A"
    await message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command("anime"))
async def anime(client, message):
    search = extract_arg(message)
    if not search:
        await message.reply_text("Format : /anime < anime name >")
        return
    variables = {"search": search}
    json = requests.post(
        url, json={"query": anime_query, "variables": variables}
    ).json()
    if "errors" in json.keys():
        await message.reply_text("Anime not found")
        return
    if json:
        json = json["data"]["Media"]
        msg = f"{json['title']['romaji']} ({json['title']['native']})\nType: {json['format']}\nStatus: {json['status']}\nEpisodes: {json.get('episodes', 'N/A')}\nDuration: {json.get('duration', 'N/A')} Per Ep.\nScore: {json['averageScore']}\nGenres: "
        for x in json["genres"]:
            msg += f"{x}, "
        msg = msg[:-2] + "\n"
        msg += "Studios: "
        for x in json["studios"]["nodes"]:
            msg += f"{x['name']}, "
        msg = msg[:-2] + "\n"
        info = json.get("siteUrl")
        trailer = json.get("trailer", None)
        json["id"]
        if trailer:
            trailer_id = trailer.get("id", None)
            site = trailer.get("site", None)
            if site == "youtube":
                trailer = "https://youtu.be/" + trailer_id
        description = (
            json.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
        )
        msg += shorten(description, info)
        image = json.get("bannerImage", None)
        if trailer:
            buttons = [
                [
                    InlineKeyboardButton("More Info", url=info),
                    InlineKeyboardButton("Trailer", url=trailer),
                ]
            ]
        else:
            buttons = [[InlineKeyboardButton("More Info", url=info)]]
        if image:
            try:
                await message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except:
                msg += f" [Image]({image})"
                await message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        else:
            await message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )



@app.on_message(filters.command("character"))
async def character(client, message):
    search = extract_arg(message)
    if not search:
        await message.reply_text("Format : /character < character name >")
        return
    variables = {"query": search}
    json = requests.post(
        url, json={"query": character_query, "variables": variables}
    ).json()
    if "errors" in json.keys():
        await message.reply_text("Character not found")
        return
    if json:
        json = json["data"]["Character"]
        msg = f"{json.get('name').get('full')} ({json.get('name').get('native')})\n"
        description = f"{json['description']}"
        site_url = json.get("siteUrl")
        msg += shorten(description, site_url)
        image = json.get("image", None)
        if image:
            image = image.get("large")
            await message.reply_photo(
                photo=image,
                caption=msg.replace("<b>", "</b>"),
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await message.reply_text(
                msg.replace("<b>", "</b>"), parse_mode=ParseMode.MARKDOWN,
            )

@app.on_message(filters.command("manga"))
async def manga(client, message):
    search = extract_arg(message)
    if not search:
        await message.reply_text("Format : /manga < manga name >")
        return
    variables = {"search": search}
    json = requests.post(
        url, json={"query": manga_query, "variables": variables}
    ).json()
    if "errors" in json.keys():
        await message.reply_text("Manga not found")
        return
    if json:
        json = json["data"]["Media"]
        msg = f"{json['title']['romaji']} ({json['title']['native']})\nType: {json['format']}\nStatus: {json['status']}\nChapters: {json.get('chapters', 'N/A')}\nScore: {json['averageScore']}\nGenres: "
        for x in json["genres"]:
            msg += f"{x}, "
        msg = msg[:-2] + "\n"
        info = json.get("siteUrl")
        json["id"]
        description = (
            json.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
        )
        msg += shorten(description, info)
        image = json.get("bannerImage", None)
        buttons = [[InlineKeyboardButton("More Info", url=info)]]
        if image:
            try:
                await message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except:
                msg += f" [Image]({image})"
                await message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        else:
            await message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )





