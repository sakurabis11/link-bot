from pyrogram import Client, filters
import os, wget
import re

@Client.on_message(filters.regex(r"^https://pin.it"))
async def pinterest(client, message):
    pint_url = messsage.text
    SD=await message.reply_text("Downloading...")
    wget.download(pint_url)
    sd=await SD.edit("Uploading...")
    await client.send_photo(message.chat.id, photo=f"{pint_url}.jpg")
    
    
