import pyrogram
from pyrogram import Client, filters
from googlesearch import search
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command(["ott"]))
async def ott_search(client, message):
    query = message.text.split(" ", 1)[1]  
    results = f"https://www.google.com/search?q={query}+ott+release+date+platform"
    url = results[0]

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        release_date = soup.find("meta", itemprop="datePublished").get("content")
        platform = soup.find("meta", itemprop="url").get("content")  
        imdb_poster_url = soup.find("meta", property="og:image").get("content")
        
        poster_file = await client.download_media(imdb_poster_url)
        await message.reply_photo(photo=poster_file, caption=f"**Title:** {query}\n**Release Date:** {release_date}\n**Platform:** {platform}")

    except Exception as e:
        await message.reply_text(f"Error: {e}")


