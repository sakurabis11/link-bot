from PIL import Image
import io
from pyrogram import Client, filters

@Client.on_message(filters.photo)
async def create_sticker(client, message):
    if message.reply_to_message.photo:
            try:
                photo = filters.photo
                with open(photo, "rb") as sticker:
                    await message.reply_sticker(sticker) 
                    await message.reply_text("Photo converted to sticker and sent!")
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")
