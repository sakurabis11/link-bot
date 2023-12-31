import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command("search", prefixes="/"))
async def search_ott(client, message):
    query = message.text.split(" ", 1)[1]  

    try:
        url = f"https://www.google.com/search?q={query} ott release date platform"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        release_date = ""
        platform = ""

        # Find release date and platform information from search results
        for result in soup.find_all("div", class_="tF2Cxc"):
            if "Release Date" in result.text:
                release_date = result.text.split(":")[1].strip()
            elif "Platform" in result.text:
                platform = result.text.split(":")[1].strip()

        await message.reply_text(
            f"**Here's what I found for {query}:**\n\n"
            f"**Release Date:** {release_date}\n"
            f"**Platform:** {platform}"
        )
    except Exception as e:
        await message.reply_text(f"Sorry, I couldn't find information for {query}. Please try again or check your internet connection.")


