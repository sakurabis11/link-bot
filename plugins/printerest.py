import os
import wget
import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.regex(r"^https?://pin\.it/([^/?]+)"))
async def pinterest(client, message: Message):
    try:
        pint_url = message.text
        SD_BOTS = await message.reply_text("Downloading...")

        response = requests.get(pint_url)
        media_url = re.search(r'"og:image" content="(.*?)"', response.text).group(1)
        media_filename = wget.download(media_url)
        
        await asyncio.sleep(5)
        await SD_BOTS.edit("Uploading...")        
      
        await client.send_document(message.chat.id, media_filename)
        
        await SD_BOTS.delete()
        os.remove(media_filename)
    except Exception as e:
        await message.reply_text(f"{e}")
