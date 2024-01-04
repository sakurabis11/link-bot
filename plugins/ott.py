import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters

@Client.on_message(filters.command("check"))
async def search(client, message):
    query = message.text.split(" ", 1)[1]
    url = f"https://www.google.com/search?q={query}+ott+release+date+platform"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.text, "html.parser")
        # Use BeautifulSoup to extract the desired information from the parsed HTML
        # (replace this with appropriate logic for your specific needs)
        result = soup.find("h3", class_="r").text

        await message.reply_text(result)

    except requests.exceptions.RequestException as e:
        await message.reply_text("An error occurred: " + str(e))

    except AttributeError:
        await message.reply_text("No relevant result found")
