import asyncio
from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("tgsticker"))
async def google_text(client, message):
    try:
        user_query = message.text.split()[1:]
        encoded_query = user_query.replace(" ", "%20")

        response = requests.get(f"https://api.safone.dev/tgsticker?query={encoded_query}&limit=1")
        if response.status_code == 200:
            data = response.json()
            sticker = data['results'][0]
            link = sticker['link']
            await client.send_message(message.chat.id, text=f"{link}")

    except Exception as e:
       await message.reply_text(f"An error occurred: {e}")
