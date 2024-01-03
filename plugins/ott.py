import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup


@Client.on_message(filters.command(["ott"]))
async def get_ott_info(client, message):
    query = message.text.split(" ", 1)[1]  # Extract the movie/series name

    try:
        url = f"https://www.google.com/search?q=ott+release+date+{query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        await message.reply_text(url)
