import os
import cv2
from PIL import Image
from telethon import events
from Bad import Bad


@Bad.on(events.NewMessage(pattern="^/tiny ?(.*)"))
async def tiny(event):
    reply = await event.get_reply_message()
    if not (reply and reply.media):
        await event.reply("Please reply to a sticker or media.")
        return

    processing_message = await event.reply("Processing...")

    downloaded_file = await Bad.download_media(reply)
    overlay_image = Image.open("assets/kang.png")

    try:
        if downloaded_file.endswith(".tgs"):
            await Bad.download_media(reply, "input.tgs")
            os.system("lottie_convert.py input.tgs temp.json")
            
            with open("temp.json", "r") as json_file:
                json_data = json_file.read().replace("512", "2000")
            
            with open("temp.json", "w") as json_file:
                json_file.write(json_data)
            
            os.system("lottie_convert.py temp.json output.tgs")
            output_file = "output.tgs"
            os.remove("temp.json")
        
        elif downloaded_file.endswith((".gif", ".mp4")):
            video = cv2.VideoCapture(downloaded_file)
            success, frame = video.read()
            if success:
                cv2.imwrite("frame.png", frame)
                img = Image.open("frame.png")
                resized_file = resize_image(img, overlay_image)
                output_file = save_overlay(resized_file, overlay_image)
                os.remove("frame.png")
        
        else:
            img = Image.open(downloaded_file)
            resized_file = resize_image(img, overlay_image)
            output_file = save_overlay(resized_file, overlay_image)
        
        await Bad.send_file(event.chat_id, output_file, reply_to=reply.id)
    
    except Exception as e:
        await event.reply(f"An error occurred: {str(e)}")
    
    finally:
        await processing_message.delete()
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)
        if os.path.exists(output_file):
            os.remove(output_file)


def resize_image(img, overlay):
    z, d = img.size
    if z == d:
        size = (200, 200)
    else:
        ratio_sum = z + d
        aspect_ratio = (z / ratio_sum, d / ratio_sum)
        size = (int(200 + 5 * ((aspect_ratio[0] * 100) - 50)), int(200 + 5 * ((aspect_ratio[1] * 100) - 50)))
    
    return img.resize(size, Image.ANTIALIAS)


def save_overlay(resized_image, overlay):
    overlay_copy = overlay.copy()
    overlay_copy.paste(resized_image, (150, 0))
    output_file = "output.webp"
    overlay_copy.save(output_file, "WEBP", quality=95)
    return output_file
