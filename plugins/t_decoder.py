from pyrogram import Client, filters
import re
import requests
import os, asyncio
import time
from pyrogram.types import *
from telegraph import upload_file

@Client.on_message(filters.regex(r"^https://telegra.ph/file/"))
async def download(client, message):
 try:
    url = message.text
    response = requests.get(url, stream=True)
    if message.text.endswith('.jpg'):

        if response.status_code == 200:
            with open('image.JPEG', 'wb') as f:
                f.write(response.content)

            await message.reply_photo(photo='image.JPEG')
            os.remove('image.JPEG')
    elif message.text.endswith('.mp4'):
        if response.status_code == 200:
            with open('video.mp4', 'wb') as f:
                f.write(response.content)
            await message.reply_video(video='video.mp4')
            os.remove('video.mp4')
        else:      
            await message.reply_text('Failed to decode the telegraph link.')
    else:
        return
 except Exception as e:
        await message.reply_text(f"{e}")

@Client.on_message(filters.command("imagine"))
async def imagine(client, message):
    try:
        url = "https://waifu.pics/sfw/waifu"
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open('image.jpg', 'wb') as f:
                f.write(response.content)

            t_send = upload_file('image.jpg')
            t_link = f"https://telegra.ph{t_send[0]}"

            await messsage.reply_text(t_link)
    except Exception as e:
        await message.reply_text(str(e))

