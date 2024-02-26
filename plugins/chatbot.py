import asyncio
from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("aichat"))
async def google_text(client, message):
    try:
        user_query = message.text.split()[1:]
        encoded_query = " ".join(user_query).replace(" ", "%20")
        response = requests.get(f"https://api.safone.dev/chatbot?query={encoded_query}&user_id=345324&bot_name=mrtg&bot_master=mrtg")
        if response.status_code == 200:
            data = response.json()
            chat_bot = data['results'][0]
            ai = f"{chat_bot['response']}"

            await message.reply_message(ai)
    except Exception as e:
       await message.reply_text(f"An error occurred: {e}")
          
