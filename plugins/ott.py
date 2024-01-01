import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup


@Client.on_message(filters.command(["ott"]))
async def get_ott_info(client, message):
    query = message.text.split(" ", 1)[1]  # Extract the movie/series name

    try:
        url = f"https://www.google.com/search?q=ott+release+date+{query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the relevant information block
        result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")

        if result:
            # Extract the release date and platform
            release_date = result.find("span", class_="LrzXr").text.strip()
            platform = result.find("div", class_="wwUB2c").text.strip()

            await message.reply_text(f"**Release Date:** {release_date}\n**Platform:** {platform}")
        else:
            await message.reply_text("Sorry, I couldn't find information for that movie/series.")
    except Exception as e:
        await message.reply_text("An error occurred while searching. Please try again later.")

