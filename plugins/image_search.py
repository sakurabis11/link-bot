import asyncio
from pyrogram import Client, filters
import requests
import wget 


@Client.on_message(filters.command("pic"))
async def google_text(client, message):
    try:
        user_query = ' '.join(message.command[1:])
        encoded_query = user_query.replace(" ", "%20")

        response = requests.get(f"https://api.safone.dev/image?query={encoded_query}&limit=1")
        if response.status_code == 200:
            data = response.json()
            image_data = data['results'][0]
            image_url = image_data['imageUrl']
            downloaded_image = wget.download(image_url)
            await client.send_photo(message.chat.id, downloaded_image)

    except Exception as e:
       await message.reply_text(f"An error occurred: {e}")
