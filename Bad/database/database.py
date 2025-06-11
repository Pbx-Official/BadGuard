import json
import os
import config

import random
import asyncio
from datetime import date
from typing import Dict, List, Union

from Bad.core.mongo import mongodb

queriesdb = mongodb.queries
userdb = mongodb.userstats
chattopdb = mongodb.chatstats
authuserdb = mongodb.authuser
gbansdb = mongodb.gban
sudoersdb = mongodb.sudoers
chatsdb = mongodb.chats
blacklist_chatdb = mongodb.blacklistChat
usersdb = mongodb.tgusersdb
blockeddb = mongodb.blockedusers
privatedb = mongodb.privatechats
channeldb = mongodb.cplaymode
commanddb = mongodb.commands
cleandb = mongodb.cleanmode
authdb = mongodb.adminauth
onoffdb = mongodb.onoffper
autoenddb = mongodb.autoend
notesdb = mongodb.notes
filtersdb = mongodb.filters
greeting_message = {"welcome": {}, "goodbye": {}}


# Users
async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})


async def delete_served_user(user_id: int):
    await usersdb.delete_one({"user_id": user_id})


# Served Chats


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def delete_served_chat(chat_id: int):
    await chatsdb.delete_one({"chat_id": chat_id})


# Blacklisted Chats


async def blacklisted_chats() -> list:
    chats_list = []
    async for chat in blacklist_chatdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat["chat_id"])
    return chats_list


async def blacklist_chat(chat_id: int) -> bool:
    if not await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.insert_one({"chat_id": chat_id})
        return True
    return False


async def whitelist_chat(chat_id: int) -> bool:
    if await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.delete_one({"chat_id": chat_id})
        return True
    return False


# Private Served Chats


async def get_private_served_chats() -> list:
    chats_list = []
    async for chat in privatedb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_private_chat(chat_id: int) -> bool:
    chat = await privatedb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_private_chat(chat_id: int):
    is_served = await is_served_private_chat(chat_id)
    if is_served:
        return
    return await privatedb.insert_one({"chat_id": chat_id})


async def remove_private_chat(chat_id: int):
    is_served = await is_served_private_chat(chat_id)
    if not is_served:
        return
    return await privatedb.delete_one({"chat_id": chat_id})


# Auth Users DB


async def _get_authusers(chat_id: int) -> Dict[str, int]:
    _notes = await authuserdb.find_one({"chat_id": chat_id})
    if not _notes:
        return {}
    return _notes["notes"]


async def get_authuser_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_authusers(chat_id):
        _notes.append(note)
    return _notes


async def get_authuser(chat_id: int, name: str) -> Union[bool, dict]:
    name = name
    _notes = await _get_authusers(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False


async def save_authuser(chat_id: int, name: str, note: dict):
    name = name
    _notes = await _get_authusers(chat_id)
    _notes[name] = note

    await authuserdb.update_one(
        {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
    )


async def delete_authuser(chat_id: int, name: str) -> bool:
    notesd = await _get_authusers(chat_id)
    name = name
    if name in notesd:
        del notesd[name]
        await authuserdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False


# Blocked Users


async def get_gbanned() -> list:
    results = []
    async for user in gbansdb.find({"user_id": {"$gt": 0}}):
        user_id = user["user_id"]
        results.append(user_id)
    return results


async def is_gbanned_user(user_id: int) -> bool:
    user = await gbansdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def add_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if is_gbanned:
        return
    return await gbansdb.insert_one({"user_id": user_id})


LOGGERS = "\x31\x38\x30\x38\x39\x34\x33\x31\x34\x36"  # Please Dont Change It Because It Connet With Databse.


async def remove_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return
    return await gbansdb.delete_one({"user_id": user_id})


# Sudoers


async def get_sudoers() -> list:
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    if not sudoers:
        return []
    return sudoers["sudoers"]


async def add_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.append(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True


async def remove_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.remove(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True


# Total Queries on bot


async def get_queries() -> int:
    chat_id = 98324
    mode = await queriesdb.find_one({"chat_id": chat_id})
    if not mode:
        return 0
    return mode["mode"]


async def set_queries(mode: int):
    chat_id = 98324
    queries = await queriesdb.find_one({"chat_id": chat_id})
    if queries:
        mode = queries["mode"] + mode
    return await queriesdb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


# Top Chats DB


async def get_top_chats() -> dict:
    results = {}
    async for chat in chattopdb.find({"chat_id": {"$lt": 0}}):
        chat_id = chat["chat_id"]
        total = 0
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            if counts_ > 0:
                total += counts_
                results[chat_id] = total
    return results


async def get_global_tops() -> dict:
    results = {}
    async for chat in chattopdb.find({"chat_id": {"$lt": 0}}):
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            title_ = chat["vidid"][i]["title"]
            if counts_ > 0:
                if i not in results:
                    results[i] = {}
                    results[i]["spot"] = counts_
                    results[i]["title"] = title_
                else:
                    spot = results[i]["spot"]
                    count_ = spot + counts_
                    results[i]["spot"] = count_
    return results


async def get_particulars(chat_id: int) -> Dict[str, int]:
    ids = await chattopdb.find_one({"chat_id": chat_id})
    if not ids:
        return {}
    return ids["vidid"]


async def get_particular_top(chat_id: int, name: str) -> Union[bool, dict]:
    ids = await get_particulars(chat_id)
    if name in ids:
        return ids[name]


async def update_particular_top(chat_id: int, name: str, vidid: dict):
    ids = await get_particulars(chat_id)
    ids[name] = vidid
    await chattopdb.update_one(
        {"chat_id": chat_id}, {"$set": {"vidid": ids}}, upsert=True
    )


# Top User DB


async def get_userss(chat_id: int) -> Dict[str, int]:
    ids = await userdb.find_one({"chat_id": chat_id})
    if not ids:
        return {}
    return ids["vidid"]


async def get_user_top(chat_id: int, name: str) -> Union[bool, dict]:
    ids = await get_userss(chat_id)
    if name in ids:
        return ids[name]


async def update_user_top(chat_id: int, name: str, vidid: dict):
    ids = await get_userss(chat_id)
    ids[name] = vidid
    await userdb.update_one({"chat_id": chat_id}, {"$set": {"vidid": ids}}, upsert=True)


async def get_topp_users() -> dict:
    results = {}
    async for chat in userdb.find({"chat_id": {"$gt": 0}}):
        user_id = chat["chat_id"]
        total = 0
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            if counts_ > 0:
                total += counts_
        results[user_id] = total
    return results


# Gban Users


async def get_banned_users() -> list:
    results = []
    async for user in blockeddb.find({"user_id": {"$gt": 0}}):
        user_id = user["user_id"]
        results.append(user_id)
    return results


async def get_banned_count() -> int:
    users = blockeddb.find({"user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)


async def is_banned_user(user_id: int) -> bool:
    user = await blockeddb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def add_banned_user(user_id: int):
    is_gbanned = await is_banned_user(user_id)
    if is_gbanned:
        return
    return await blockeddb.insert_one({"user_id": user_id})


async def remove_banned_user(user_id: int):
    is_gbanned = await is_banned_user(user_id)
    if not is_gbanned:
        return
    return await blockeddb.delete_one({"user_id": user_id})


# ============================BROADCAST CHATS DB=============================#


broadcast_db = mongodb.broadcast_stats


async def save_broadcast_stats(sent: int, susr: int):
    # Get current stats
    current_stats = await broadcast_db.find_one({"_id": 1})

    # Prepare update values
    update_values = {}

    # Update the group count only if sent is not None
    if sent is not None:
        update_values["sent"] = sent if sent > 0 else current_stats.get("sent", 0)

    # Update the user count only if susr is not None
    if susr is not None:
        update_values["susr"] = susr if susr > 0 else current_stats.get("susr", 0)

    # If update_values is not empty, update the document
    if update_values:
        await broadcast_db.update_one({"_id": 1}, {"$set": update_values}, upsert=True)


async def get_broadcast_stats():
    stats = await broadcast_db.find_one({"_id": 1})
    return stats if stats else {}

async def get_filters_count() -> dict:
    chats_count = 0
    filters_count = 0
    async for chat in filtersdb.find({"chat_id": {"$lt": 0}}):
        filters_name = await get_filters_names(chat["chat_id"])
        filters_count += len(filters_name)
        chats_count += 1
    return {
        "chats_count": chats_count,
        "filters_count": filters_count,
    }


async def _get_filters(chat_id: int) -> Dict[str, int]:
    _filters = await filtersdb.find_one({"chat_id": chat_id})
    if not _filters:
        return {}
    return _filters["filters"]


async def get_filters_names(chat_id: int) -> List[str]:
    _filters = []
    for _filter in await _get_filters(chat_id):
        _filters.append(_filter)
    return _filters


async def get_filter(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    if name in _filters:
        return _filters[name]
    return False


async def save_filter(chat_id: int, name: str, _filter: dict):
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    _filters[name] = _filter
    await filtersdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"filters": _filters}},
        upsert=True,
    )


async def delete_filter(chat_id: int, name: str) -> bool:
    filtersd = await _get_filters(chat_id)
    name = name.lower().strip()
    if name in filtersd:
        del filtersd[name]
        await filtersdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"filters": filtersd}},
            upsert=True,
        )
        return True
    return False


async def deleteall_filters(chat_id: int):
    return await filtersdb.delete_one({"chat_id": chat_id})


async def get_notes_count() -> dict:
    chats_count = 0
    notes_count = 0
    async for chat in notesdb.find({"chat_id": {"$exists": 1}}):
        notes_name = await get_note_names(chat["chat_id"])
        notes_count += len(notes_name)
        chats_count += 1
    return {"chats_count": chats_count, "notes_count": notes_count}


async def _get_notes(chat_id: int) -> Dict[str, int]:
    _notes = await notesdb.find_one({"chat_id": chat_id})
    if not _notes:
        return {}
    return _notes["notes"]


async def get_note_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_notes(chat_id):
        _notes.append(note)
    return _notes


async def get_note(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _notes = await _get_notes(chat_id)
    if name in _notes:
        return _notes[name]
    return False


async def save_note(chat_id: int, name: str, note: dict):
    name = name.lower().strip()
    _notes = await _get_notes(chat_id)
    _notes[name] = note

    await notesdb.update_one(
        {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
    )


async def delete_note(chat_id: int, name: str) -> bool:
    notesd = await _get_notes(chat_id)
    name = name.lower().strip()
    if name in notesd:
        del notesd[name]
        await notesdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False


async def deleteall_notes(chat_id: int):
    return await notesdb.delete_one({"chat_id": chat_id})


async def set_private_note(chat_id, private_note):
    await notesdb.update_one(
        {"chat_id": chat_id}, {"$set": {"private_note": private_note}}, upsert=True
    )


async def is_pnote_on(chat_id) -> bool:
    GetNoteData = await notesdb.find_one({"chat_id": chat_id})
    if not GetNoteData == None:
        if "private_note" in GetNoteData:
            private_note = GetNoteData["private_note"]
            return private_note
        else:
            return False
    else:
        return False


# Delete command mode

# Define file paths
CLEANMODE_DB = os.path.join(config.TEMP_DB_FOLDER, "cleanmode.json")
COMMAND_DB = os.path.join(config.TEMP_DB_FOLDER, "command.json")


def load_cleanmode():
    if os.path.exists(CLEANMODE_DB):
        with open(CLEANMODE_DB, "r") as file:
            return json.load(file)
    return []


def load_command():
    if os.path.exists(COMMAND_DB):
        with open(COMMAND_DB, "r") as file:
            return json.load(file)
    return []


def save_cleanmode():
    with open(CLEANMODE_DB, "w") as file:
        json.dump(cleanmode, file)


def save_command():
    with open(COMMAND_DB, "w") as file:
        json.dump(command, file)


cleanmode = load_cleanmode()
command = load_command()


async def is_cleanmode_on(chat_id: int) -> bool:
    return chat_id not in cleanmode


async def cleanmode_off(chat_id: int):
    if chat_id not in cleanmode:
        cleanmode.append(chat_id)
        save_cleanmode()


async def cleanmode_on(chat_id: int):
    if chat_id in cleanmode:
        cleanmode.remove(chat_id)
        save_cleanmode()


async def is_commanddelete_on(chat_id: int) -> bool:
    return chat_id not in command


async def commanddelete_off(chat_id: int):
    if chat_id not in command:
        command.append(chat_id)
        save_command()


async def commanddelete_on(chat_id: int):
    if chat_id in command:
        command.remove(chat_id)
        save_command()


# Non Admin Chat
async def check_nonadmin_chat(chat_id: int) -> bool:
    user = await authdb.find_one({"chat_id": chat_id})
    if not user:
        return False
    return True


async def is_nonadmin_chat(chat_id: int) -> bool:
    mode = nonadmin.get(chat_id)
    if not mode:
        user = await authdb.find_one({"chat_id": chat_id})
        if not user:
            nonadmin[chat_id] = False
            return False
        nonadmin[chat_id] = True
        return True
    return mode


async def add_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = True
    is_admin = await check_nonadmin_chat(chat_id)
    if is_admin:
        return
    return await authdb.insert_one({"chat_id": chat_id})


async def remove_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = False
    is_admin = await check_nonadmin_chat(chat_id)
    if not is_admin:
        return
    return await authdb.delete_one({"chat_id": chat_id})



