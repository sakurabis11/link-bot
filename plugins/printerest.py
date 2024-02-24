import os
import re
import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.regex(r"^https?://pin\.it/([^/?]+)"))
async def pinterest(client, message: Message):
    try:
        pint_url = message.text
        SD_BOTS = await message.reply_text("Downloading...")
        response = requests.get(pint_url, allow_redirects=True)
        if response.status_code == 200:
            filename = "pinterest_image.jpg"
            with open(filename, "wb") as f:
                f.write(response.content)
            await asyncio.sleep(5)
            await SD_BOTS.edit("Uploading...")
            await SD_BOTS.delete()
            await client.send_focument(message.chat.id, filename)
    except Exception as e:
            await message.reply_text(f"{e}")
