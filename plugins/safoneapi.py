import asyncio
from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("google"))
async def google_text(client, message):
 try:
    query = ' '.join(message.command[1:])
    query = query.replace(" ","%20")
    await message.reply_text(f"query")
  
    response = requests.get(f"https://api.safone.dev/image?query={query}&limit=1")
    if response.status_code == 200:
        data = response.json()
        g_result = data['items'][0]
        reply = f"{g_result['imageUrl']}"
        photo = wget.download(reply)
        await client.send_message(message.chat.id, photo)
          
 except Exception as e:
        await message.reply_text(f"{e}")
  
