import os
import re
import wget
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.regex(r"^https?://pin.it/([^/?]+"))
async def pinterest(client, message: Message):
 try:
     pint_url = message.text
     SD_BOTS = await message.reply_text("Downloading...")
     await asyncio.sleep(5)
     await SD_BOTS.edit("Uploading...")
     await client.send_document(message.chat.id, pint_url)
     await SD.delete()
     os.remove(thumbnail)
 except Exception as e:
     await message.reply_text(f"{e}")
