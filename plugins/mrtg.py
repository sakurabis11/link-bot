from pyrogram import Client, filters
from requests import get
import os

@Client.on_message(filters.command("mrtg"))
async def download(client, message):
    try:
        url = message.text.split()[1]
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open("image.JPEG",'rb') as f:
                f.write(get(link).content)
            await message.reply_photo(photo='image.JPEG')
            os.remove('image.JPEG')
        else:
            await message.reply_text('Failed to download image.')
    except Exception as e:
        await message.reply_text(f"{e}")
