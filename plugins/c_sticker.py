from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image
from io import BytesIO
from utils import convert_photo_to_sticker

@Client.on_message(filters.command("c"))
async def photo_to_sticker(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo
        file_id = photo.file_id
        file_path = await client.download_media(file_id)

        sticker = convert_photo_to_sticker(file_path)
        await client.send_sticker(message.chat_id, sticker)
    else:
        await message.reply_text("Please reply to a photo with the /c command.")
