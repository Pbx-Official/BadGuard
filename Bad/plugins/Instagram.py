from pyrogram import filters, Client
import bs4
import requests
import re
import asyncio
import os
import traceback
import random
from Bad import app



@app.on_message(filters.command(["ig", "reel", "reels", "insta"], prefixes=["/", "!", "."]))
async def instadownload(client, message):
    await message.reply_text(f" ok now send me your url ")




headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "99",
    "Origin": "https://saveig.app",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

@app.on_message(filters.regex(r'https?://.*instagram[^\s]+') & (filters.private | filters.group))
async def link_handler(app, message):
    link = message.matches[0].group(0)
    global headers
    try:
        url= link.replace("instagram.com", "ddinstagram.com")
        url=url.replace("==","%3D%3D")
        if url.endswith("="):
           await message.reply_video(url[:-1])
        else:
           await message.reply_video(url)
    except Exception as e:
        try:
            if "/reel/" in url:
               ddinsta=True 
               getdata = requests.get(url).text
               soup = bs4.BeautifulSoup(getdata, 'html.parser')
               meta_tag = soup.find('meta', attrs={'property': 'og:video'})
               try:
                  content_value =f"https://ddinstagram.com{meta_tag['content']}"
               except:
                   pass 
               if not meta_tag:
                  ddinsta=False
                  meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)

                  if meta_tag.ok:
                     res=meta_tag.json()


                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                     content_value = meta[0]
                  else:
                      return await message.reply("oops something went wrong")
               try:
                   if ddinsta:
                      await message.reply_video(content_value)
                   else:
                       await message.reply_video(content_value)
               except:
                   downfile=f"{os.getcwd()}/{random.randint(1,10000000)}"
                   with open(downfile,'wb') as x:
                       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                       x.write(requests.get(content_value,headers=headers).content)
                   await message.reply_video(downfile) 
            elif "/p/" in url:
                  meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                  if meta_tag.ok:
                     res=meta_tag.json()
                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                  else:
                      return await message.reply("oops something went wrong")

                  for i in range(len(meta) - 1):
                     com=await message.reply_text(meta[i])
                     await asyncio.sleep(0.001)
                     try:
                        await message.reply_video(com.text)
                        await com.delete()
                     except:
                         pass 
            elif "stories" in url:
                  meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                  if meta_tag.ok:
                     res=meta_tag.json()
                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                  else:
                      return await message.reply("Oops something went wrong")
                  try:
                     await message.reply_video(meta[0])
                  except:
                      com=await message.reply(meta[0])
                      await asyncio.sleep(0.001)
                      try:
                          await message.reply_video(com.text)
                          await com.delete()
                      except:
                          pass

        except KeyError:
            await message.reply(f"400: Sorry, Unable To Find It Make Sure Its Publically Available :)")
        except Exception as e:

            await message.reply(f"400: Sorry, Unable To Find It  try another. ")

        finally:
            if 'downfile' in locals():
                os.remove(downfile)

