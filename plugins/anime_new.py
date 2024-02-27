import asyncio
from pyrogram import Client, filters
import requests
import wget 

@Client.on_message(filters.command("anime_news"))
async def google_text(client, message):
    try: 
        response = requests.get(f"https://api.safone.dev/anime/news?limit=1")
        if response.status_code == 200:
            data = response.json()
            image_data = data['results'][0]
            text_data = image_data['description']
            title_data = image_data['title']
            image_url = image_data['imageUrl']
            downloaded_image = wget.download(image_url)
            await client.send_photo(message.chat.id, downloaded_image, caption=f"Title: {title_data}\n\nNews: {text_data}")
            await client.send_message(REQUESTED_CHANNEL, text=f"#ᴀɴɪᴍᴇ_ɴᴇᴡs\nʀǫᴜᴇsᴛᴇᴅ: {message.from_user.mention}")

    except Exception as e:
       await message.reply_text(f"An error occurred: {e}")
