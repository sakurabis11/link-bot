import asyncio
from SafoneAPI import SafoneAPI
from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("google"))
async def google_text(client, message):
 try:
    query = ' '.join(message.command[1:])
    query = query.replace(" ","%20")
    response = requests.get(f"https://api.safone.dev/google?query={query}&limit=1")
    if response.status_code == 200:
        data = response.json()
        if data['total_count'] > 0:
          g_result = data['items'][0]
          reply = f"**🔖 ᴅᴇsᴄʀɪᴘᴛɪᴏɴ:** <code>{g_result['description']}</code>\n"
          await message.reply_text(reply)
          
 except Exception as e:
          await message.reply_text(f"{e}")
  
