import sys
from os import getenv

from dotenv import load_dotenv
from pyrogram import Client, filters
import random
import re

load_dotenv()

BANNED_USERS = filters.user()



# ________________________________________________________________________________#
# Get it from my.telegram.org
API_ID = 12380656
API_HASH = "d927c13beaaf5110f25c505b7c071273"
BOT_USERNAME ="Broken_Bot"

# ________________________________________________________________________________#
## Get it from @Botfather in Telegram.
BOT_TOKEN = "7436017266:AAEdGRwaM6WXsod3bV3qGIboCZIeJiLAXOk"

# ________________________________________________________________________________#
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# You have to Enter the app name which you gave to identify your  Music Bot in Heroku.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

# ________________________________________________________________________________#
# Database to save your chats and stats... Get MongoDB:-  https://telegra.ph/How-To-get-Mongodb-URI-04-06
DB_NAME = "BadDB"
MONGO_DB_URI = "mongodb+srv://karan69:karan69@cluster0.gfw7e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# ________________________________________________________________________________#
# You'll need a Private Group ID for this.
LOG_GROUP_ID = -1002093247039

# ________________________________________________________________________________#

# Your User ID.
OWNER_ID = list(
    map(int, getenv("OWNER_ID", "7588172591").split())
)  # Input type must be interger


# ________________________________________________________________________________#
# For customized or modified Repository

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/Pbx-Official/BadGuard",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")

GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

EXTRA_PLUGINS = getenv(
    "EXTRA_PLUGINS",
    "Fasle",
)

# Fill True if you want to load extra plugins


EXTRA_PLUGINS_REPO = getenv(
    "EXTRA_PLUGINS_REPO",
    "https://github.com",
)
# Fill here the external plugins repo where plugins that you want to load


EXTRA_PLUGINS_FOLDER = getenv("EXTRA_PLUGINS_FOLDER", "plugins")

# Your folder name in your extra plugins repo where all plugins stored

# Time zone (india)
TIME_ZONE = "Asia/Kolkata"
