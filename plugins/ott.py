import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup


@Client.on_message(filters.command("ott"))
async def ott_search(client, message):
    try:
        query = message.text.split(" ", 1)[1]
        release_date, platform = await search_ott_info(query)
        await message.reply_text(f"Release date: {release_date}\nPlatform: {platform}")
    except Exception as e:
        await message.reply_text("Something went wrong. Please try again later.")
        print(f"Error: {e}")

async def search_ott_info(query):
    url = f"https://www.google.com/search?q={query}+ott+release+date+platform"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    results = soup.find_all("div", class_="g")
    for result in results:
        release_date = result.find("span", class_="aCOpRe").text
        platform = result.find("cite").text
        if release_date and platform:
            return release_date, platform

