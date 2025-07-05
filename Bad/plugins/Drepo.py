import os
import shutil

import git
from pyrogram import filters

from Bad import app
import aiohttp
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@app.on_message(filters.command(["downloadrepo"]))
def download_repo(_, message):
    if len(message.command) != 2:
        message.reply_text(
            "Please provide the GitHub repository URL after the command. Example: /downloadrepo Repo Url "
        )
        return

    repo_url = message.command[1]
    zip_path = download_and_zip_repo(repo_url)

    if zip_path:
        with open(zip_path, "rb") as zip_file:
            message.reply_document(zip_file)
        os.remove(zip_path)
    else:
        message.reply_text("Unable to download the specified GitHub repository.")


def download_and_zip_repo(repo_url):
    try:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = f"{repo_name}"

        # Clone the repository
        repo = git.Repo.clone_from(repo_url, repo_path)

        # Create a zip file of the repository
        shutil.make_archive(repo_path, "zip", repo_path)

        return f"{repo_path}.zip"
    except Exception as e:
        print(f"Error downloading and zipping GitHub repository: {e}")
        return None
    finally:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)


@app.on_message(filters.command(["github", "git"]))
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("/git itzshukla")
        return

    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404")

            result = await request.json()

            try:
                url = result["html_url"]
                name = result["name"]
                company = result["company"]
                bio = result["bio"]
                created_at = result["created_at"]
                avatar_url = result["avatar_url"]
                blog = result["blog"]
                location = result["location"]
                repositories = result["public_repos"]
                followers = result["followers"]
                following = result["following"]

                caption = f"""❖ɢɪᴛʜᴜʙ ɪɴғᴏ ᴏғ {name} ❖
                
🔸ᴜsᴇʀɴᴀᴍᴇ: {username}
▫️ʙɪᴏ: {bio}
▪️ʟɪɴᴋ: [Here]({url})
🔸ᴄᴏᴍᴩᴀɴʏ: {company}
▫️ᴄʀᴇᴀᴛᴇᴅ ᴏɴ: {created_at}
▪️ʀᴇᴩᴏsɪᴛᴏʀɪᴇs: {repositories}
🔸ʙʟᴏɢ: {blog}
▫️ʟᴏᴄᴀᴛɪᴏɴ: {location}
▪️ғᴏʟʟᴏᴡᴇʀs: {followers}
🔸ғᴏʟʟᴏᴡɪɴɢ: {following}"""

            except Exception as e:
                print(str(e))
                pass

    # Create an inline keyboard with a close button
    close_button = InlineKeyboardButton("Close", callback_data="close")
    inline_keyboard = InlineKeyboardMarkup([[close_button]])

    # Send the message with the inline keyboard
    await message.reply_photo(
        photo=avatar_url, caption=caption, reply_markup=inline_keyboard
    )


__MODULE__ = "ɢɪᴛʜᴜʙ"
__HELP__ = """
**<u>🌐 ɢɪᴛʜᴜʙ ᴜᴛɪʟs</u>**

» `/downloadrepo <url>` – ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴᴅ ᴢɪᴘ ᴀɴʏ ɢɪᴛʜᴜʙ ʀᴇᴘᴏ ꜰʀᴏᴍ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴜʀʟ.
• ᴇxᴀᴍᴘʟᴇ: `/downloadrepo https://github.com/user/repo`

» `/git <username>` – ꜰᴇᴛᴄʜ ᴅᴇᴛᴀɪʟᴇᴅ ɪɴꜰᴏ ᴀʙᴏᴜᴛ ᴀɴʏ ɢɪᴛʜᴜʙ ᴜꜱᴇʀ.
• ɪɴᴄʟᴜᴅᴇꜱ: ɴᴀᴍᴇ, ʙɪᴏ, ʟɪɴᴋꜱ, ᴄʀᴇᴀᴛɪᴏɴ ᴅᴀᴛᴇ, ʀᴇᴘᴏꜱ, ꜰᴏʟʟᴏᴡᴇʀꜱ, ᴇᴛᴄ.

**<u>💡 ᴛɪᴘꜱ</u>**
• ᴅᴏɴ’ᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ᴘᴀꜱꜱ ᴀ ᴠᴀʟɪᴅ ɢɪᴛʜᴜʙ ʟɪɴᴋ.
• ʀᴇᴘᴏ ᴍᴜꜱᴛ ʙᴇ ᴘᴜʙʟɪᴄ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.
"""
