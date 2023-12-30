import pyrogram
from pyrogram import filters, Client
import requests 
from info import G_API_KEY
from bs4 import BeautifulSoup 

async def check_imdb_validity(query):
    url = f"https://www.imdb.com/find?q={query}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("td", class_="result_text")
        return len(results) > 0  
    except Exception as e:
        print(f"Error checking IMDb validity: {e}")
        return False

# Function to search release date and platform (using Google Search API)
async def get_release_info(query):
    api_key = G_API_KEY
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx=your_search_engine_id&q={query} release date platform"
    try:
        response = requests.get(url)
        data = response.json()
        if data["items"]:
            first_result = data["items"][0]
            return first_result["snippet"].split(" - ")[0], first_result["snippet"].split(" - ")[1]
        else:
            return None, None  # No results found
    except Exception as e:
        print(f"Error fetching release info: {e}")
        return None, None

@Client.on_message(filters.command("search"))
async def search_movie_or_series(client, message):
    query = message.text.split(" ", 1)[1]

    try:
        is_valid_imdb = await check_imdb_validity(query)
        if not is_valid_imdb:
            await message.reply("Movie or series not found on IMDb.")
            return

        release_date, platform = await get_release_info(query)
        if release_date and platform:
            await message.reply(f"Release Date: {release_date}\nPlatform: {platform}")
        else:
            await message.reply("Release date and platform information not found.")
    except Exception as e:
        print(f"Error processing search: {e}")
        await message.reply("An error occurred while processing your request.")

