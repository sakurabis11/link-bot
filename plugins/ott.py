import pyrogram
from pyrogram import Client, filters
import re
import requests

@Client.on_message(filters.command(["search"]))
async def search_movie_or_series(client, message):
    query = message.text.split(" ", 1)[1] 

    url = f"https://www.google.com/search?q={query}_release_date_platform"  
    response = requests.get(url)
    data = response.json()

    if data["Response"] == "True":
        try:
            release_date = data["Search"][0]["Year"]
            platform = "OTT platform information not available"  # Replace with logic to fetch platform
            await message.reply_text(f"{query} was released in {release_date}. It's available on {platform}")
        except IndexError:
            await message.reply_text(f"Movie/series '{query}' not found.")
    else:
        await message.reply_text(f"An error occurred while searching for '{query}'. Please try again.")

