from pyrogram import Client, filters
from bing_image_scraper import BingImageScraper

scraper = BingImageScraper(adult_filter="Off")

@Client.on_message(filters.command("bing"))
async def bing_search(client, message):
    query = message.text.split(" ")[1]
    try:
        # Search for images on Bing
        images = scraper.search(query, num_results=5)

        # Send the first image to the user
        client.send_photo(message.chat.id, images[0])
    except Exception as e:
        print(f"Error searching for images: {e}")
        client.send_message(message.chat.id, f"Sorry, I couldn't find any images for '{query}'.")


