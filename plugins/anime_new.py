import asyncio
from pyrogram import Client, filters
import requests
import wget
from info import REQUESTED_CHANNEL

@Client.on_message(filters.command("anime_news"))
async def anime_news_handler(client, message):
 try:
    user_query = ' '.join(message.command[1:])
    if not user_query:
        await message.reply_text("")
    encoded_query = user_query.replace(" ", "%20")
     
    response = requests.get(f"https://api.safone.dev/anime/news?limit=1")
    if response.status_code == 200:
      data = response.json()
      image_data = data['results'][0]
      text_data = image_data['description']
      title_data = image_data['title']
    else:
      pass

    response = requests.get(f"https://api.safone.dev/image?query={title_data}&limit=1")
    if response.status_code == 200:
      data = response.json()
      image_url = data['imageUrl']
      downloaded_image = await wget.download(image_url) 
    else:
      pass
      
      await client.send_photo(message.chat.id, downloaded_image, caption=f"Title: {title_data}\n\nNews: {text_data}")
      await client.send_message(REQUESTED_CHANNEL, text=f"#ᴀɴɪᴍᴇ_ɴᴇᴡs\nʀǫᴜᴇsᴛᴇᴅ: {message.from_user.mention}")

  except Exception as e:
    await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command("anime_news"))
async def anime_news_handler(client, message):
  await google_text(client, message)  
