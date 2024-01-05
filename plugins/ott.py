import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command("ott", prefixes="/"))
async def ott_search(client, message):
    search_query = message.text.split(" ", 1)[1]  

    try:
        url = f"https://www.google.com/search?q=ott+release+date+{search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        release_date = soup.find("span", {"class": "Z0LcW"}).text  
        platform = soup.find("div", {"class": "BNeawe s3v9rd AP7Wnd"}).text  

        await message.reply_text(f"Release Date: {release_date}\nPlatform: {platform}")
    except Exception as e:
        await message.reply_text("Something went wrong! Please try again.")


