import pyrogram
from pyrogram import Client, filters
import requests

STICKER_ID = "CAACAgUAAxkBAAIefmWa2mFflQjODv8DcWTwKN5rb7x3AAJyCgACywLBVKKgVw2dk9PbHgQ"  

@Client.on_message(filters.text & filters.regex(r"https://pin\.it/\w+"))
async def download_photo(client, message):
    try:
        await message.reply_sticker(STICKER_ID)  

        pin_url = message.text
        response = requests.get(pin_url)
        response.raise_for_status()  

        image_url = response.url  # Extract the direct image URL

        await client.send_photo(message.chat.id, image_url)  
    except Exception as e:
        await message.reply_text(f"Error downloading photo: {e}")

