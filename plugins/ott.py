import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command(["search"]))
async def search_movie_or_series(client, message):
    query = message.text.split(" ", 1)[1] 

    url = f"https://www.google.com/search?q={query}_release_date_platform"  
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            release_date = soup.find('div', {'class': 'BNeawe iBp4i AP7Wnd'}).get_text(strip=True)
            platform = "OTT platform information not available"  # Replace with logic to fetch platform
            await message.reply_text(f"{query} was released on {release_date}. It's available on {platform}")
        except AttributeError:
            await message.reply_text(f"Movie/series '{query}' not found.")
    else:
        await message.reply_text(f"An error occurred while searching for '{query}'. Please try again.")
