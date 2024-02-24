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
        media_url_match = re.search(r'"og:image" content="(.*?)"', response.text)
        
        if media_url_match:
            media_url = media_url_match.group(1)
            media_filename = wget.download(media_url)
            
            await asyncio.sleep(5)
            await SD_BOTS.edit("Uploading...")
            
            # Send the downloaded media as a document
            await client.send_document(message.chat.id, media_filename)
            
            await SD_BOTS.delete()
            os.remove(media_filename)
        else:
            await SD_BOTS.edit("No media found.")
    except Exception as e:
        await message.reply_text(f"{e}")
