import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command("search"))
async def search_movie(client, message):
    search_query = message.text.split(" ", 1)[1]  

    search_url = f"https://www.google.com/search?q={search_query}_release_date_and_platform"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    release_date = soup.find("div", class_="BNeawe s3v9rd AP7Wnd\n").text.strip()

    if release_date and platform:
        await message.reply_text(f"**{search_query}** is available on **{platform}**.\nRelease Date: **{release_date}**")
    else:
        await message.reply_text(f"I couldn't find release information for **{search_query}** on any OTT platforms.")


