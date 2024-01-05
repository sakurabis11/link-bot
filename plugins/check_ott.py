import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command("search"))
async def search_movie(client, message):
    query = message.text.split(" ", 1)[1]  

    try:
        url = f"https://www.google.com/search?q={query}+ott+release+date+and+platform"
        
        response = requests.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.content, "html.parser")
        first_result = soup.find("div", class_="tF2Cxc")

            # Format message
            message_text = f"**Movie Name:** {movie_name}\n**OTT Platform:** {ott_platform}\n**OTT Release Date:** {ott_release_date}"
            await message.reply(message_text)
