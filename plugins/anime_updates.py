import pyrogram
from pyrogram import Client
import requests
from bs4 import BeautifulSoup
import pymongo
from info import DATABASE_NAME, DATABASE_URI, COLLECTION_NAME, LOG_CHANNEL

client = pymongo.MongoClient(DATABASE_URI)  
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

CHANNEL_ID = LOG_CHANNEL

async def check_for_updates():
    try:
        response = requests.get("https://www.crunchyroll.com/videos/new")
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.content, "html.parser")
        new_anime_list = soup.find_all("div", class_="show-tile-outer")

        for anime_item in new_anime_list:
            # Extract details (modify selectors as needed)
            title = anime_item.find("h4").text.strip()
            photo_url = anime_item.find("img")["src"]
            # Fetch IMDb rating (replace with your IMDb API logic)
            imdb_rating = fetch_imdb_rating(title)

            # Check if anime is already in database
            if not collection.find_one({"title": title}):
                # Save to MongoDB
                anime_data = {
                    "title": title,
                    "photo_url": photo_url,
                    "imdb_rating": imdb_rating
                }
                collection.insert_one(anime_data)

                # Send message to Telegram channel
                photo = await bot.download_media(photo_url)
                await bot.send_photo(
                    CHANNEL_ID,
                    photo,
                    caption=f"New anime added on Crunchyroll!\nTitle: {title}\nIMDB Rating: {imdb_rating}"
                )
    except Exception as e:
        print(f"Error checking for updates: {e}")


