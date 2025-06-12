from base64 import b64decode as m
from Bad import app
import requests
import json
from pyrogram import Client, filters

def payloads_response(payloads, args):
    payloads['context'].append({"message": args, "turn": "user"})
    return payloads

payload8 = {
    "name": "chatgpt",
    "user_id": "efc90bf8-2f23-4f2f-b54a97efde511145",
    "context": [],
    "predefined": False,
    "lipsync": False,
    "send_photo": True,
    "strapi_bot_id": 848381,
    "persona_facts": ["behave as normal", "you are the official ChatGPT AI", "your owner is @itz_Cute_Shivani", "don't suggest negative content"],
    "response_emotion": "curiosity",
    "bot_pronoun": "she/her",
    "is_retry": True
}

@app.on_message(filters.command(["chatgpt", "ai", "ask", "gpt"]))
async def chatgptt(client, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "Example:\n\n`/ai which is the smallest country?`"
        )
        return
      
    if message.reply_to_message and message.reply_to_message.text:
        args = message.reply_to_message.text
    else:
        args = " ".join(message.command[1:])
    
    session = requests.Session()
    response_data = payloads_response(payloads=payload8, args=args)
    url = m("aHR0cHM6Ly9hcGkuZXhoLmFpL2NoYXRib3QvdjEvZ2V0X3Jlc3BvbnNl").decode("utf-8")
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6ImJvdGlmeS13ZWItdjMifQ.O-w89I5aX2OE_i4k6jdHZJEDWECSUfOb1lr9UdVH4oTPMkFGUNm9BNzoQjcXOu8NEiIXq64-481hnenHdUrXfg",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    response = session.post(url, headers=headers, data=json.dumps(response_data))
    
    if response.status_code == 200:
        response_json = response.json()
        if "response" in response_json:
            await message.reply_text(response_json["response"])
        else:
            await message.reply_text("sᴏʀʀʏ ᴅᴀʀʟɪɴɢ ᴛᴏᴅᴀʏ ɪs sᴇʀᴠᴇʀ ᴅᴇᴀᴅ ᴘʟᴇᴀsᴇ ᴅᴏɴ'ᴛ ᴛʀʏ ᴛᴏᴍᴏʀʀᴏᴡ 😴")
    else:
        await message.reply_text(f"........😑")

