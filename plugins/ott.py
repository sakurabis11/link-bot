import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

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


