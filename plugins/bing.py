
import os
import asyncio
from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests

@Client.on_message(filters.command("bing_search"))
async def bing_search(client, message):
    # Extract the search query from the message
    query = message.text.split(" ")[1:]
    query = " ".join(query)

    # Construct the Bing search URL
    url = f"https://www.bing.com/images/search?q={query}"

    # Send a GET request to the Bing search URL
    response = requests.get(url)

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the image URLs from the search results
    image_urls = [
        image["src"]
        for image in soup.find_all("img", {"class": "mimg"})
        if image["src"].startswith("https://")
    ]

    # Download the first image to the current directory
    image_url = image_urls[0]
    image_name = image_url.split("/")[-1]
    image_path = os.path.join(os.getcwd(), image_name)
    await asyncio.create_task(download_image(image_url, image_path))

    # Send the downloaded image to the user
    await client.send_photo(image_path)

# Define the function to download an image from a URL
async def download_image(url, path):
    async with requests.get(url) as response:
        with open(path, "wb") as f:
            f.write(await response.content.read())

