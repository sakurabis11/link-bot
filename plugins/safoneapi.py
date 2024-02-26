import asyncio
from pyrogram import Client, filters
import requests
import wget  # Added import

@Client.on_message(filters.command("google"))
async def google_text(client, message):
    try:
        user_query = ' '.join(message.command[1:])
        encoded_query = user_query.replace(" ", "%20")
        await message.reply_text(f"Query: {encoded_query}")

        response = requests.get(f"https://api.safone.dev/image?query={encoded_query}&limit=1")
        if response.status_code == 200:
            data = response.json()
            image_data = data['results'][0]
            image_url = image_data['imageUrl']
            downloaded_image = wget.download(image_url)
            await client.send_message(message.chat.id, downloaded_image)

    except Exception as e:
       await message.reply_text(f"An error occurred: {e}")
