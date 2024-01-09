import os
from pyrogram import Client
import requests

@Client.on_message(filters.command("google"))
async def google_search(client, message):
    query = message.text.split(" ", 1)[1]  

    try:
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        await message.reply_text(f"{response}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

