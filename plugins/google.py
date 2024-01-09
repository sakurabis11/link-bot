import os
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command("google"))
async def google_search(client, message):
    query = message.text.split(" ", 1)[1]  # Extract query from command

    try:
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.content, "html.parser")
        result = soup.find("div", class_="g")  # Find the first search result

        title = result.find("h3").text
        link = result.find("a")["href"]

        await message.reply_text(f"**Search Result:**\nTitle: {title}\nLink: {link}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")


