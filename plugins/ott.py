import pyrogram
from pyrogram import Client, filters
import requests
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

async def get_release_info(query):
    url = f"https://www.google.com/search?q={query}_release_date_platform"

    try:
        response = requests.get(url)
        data = response.json()
        if data["items"]:
            first_result = data["items"][0]
            return first_result["snippet"].split(" - ")[0], first_result["snippet"].split(" - ")[1]
        else:
            return None, None
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
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        await message.reply("Error fetching data. Please check your internet connection.")
    except ValueError as e:
        print(f"Error parsing data: {e}")
        await message.reply("Error processing information. Please try again later.")
    except Exception as e:
        print(f"Error processing search: {e}")
        await message.reply("An error occurred while processing your request.")


