import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

@Client.on_message(filters.command("pin") & filters.private)
async def handle_pin_command(client, message):
    try:
        # Send a sticker to indicate bot activity
        await message.reply_sticker("CAACAgUAAxkBAAIefmWa2mFflQjODv8DcWTwKN5rb7x3AAJyCgACywLBVKKgVw2dk9PbHgQ")

        pinterest_link = message.text.split(" ")[1]
        response = requests.get(pinterest_link)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract image URL from Pinterest page (adjust selector if needed)
        image_url = soup.find("img", class_="Xp9Ar").get("src")

        # Download and send the image
        image_data = requests.get(image_url).content
        await message.reply_photo(image_data)

    except Exception as e:
        await message.reply_text("Error: " + str(e))


