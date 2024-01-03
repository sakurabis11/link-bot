import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup


@Client.on_message(filters.command(["ott"]))
async def get_ott_info(client, message):
    query = message.text.split(" ", 1)[1]  # Extract the movie/series name

    url = f"https://www.google.com/search?q=ott+release+date+{query}"
        
    await message.reply_text(url)
