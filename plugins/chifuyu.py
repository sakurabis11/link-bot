import os
import logging
from pyrogram import Client, filters, enums
import requests
import json
from spotipy import Spotify
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Initialize Spotify client
sp = Spotify(auth_manager=SpotifyOAuth())

# Define the command handler for /song
@Client.on_message(filters.command("s"))
async def music(client, message):
    # Extract query from the command
    query = " ".join(message.command[1:])

    # Search songs on Spotify
    results = sp.search(query, type="track")
    if not results["tracks"]["items"]:
        await client.send_message(message.chat.id, f"No results found for '{query}' on Spotify.")
        return

    # Extract information from the first result
    track = results["tracks"]["items"][0]
    preview_url = track["preview_url"]

    # Download song preview and send as voice message
    temp_file = await download_preview(preview_url)
    await client.send_voice(chat_id=message.chat.id, voice=temp_file)
    os.remove(temp_file)

# Function to download song preview
async def download_preview(url):
    response = requests.get(url)
    with open("temp.mp3", "wb") as f:
        f.write(response.content)
    return "temp.mp3"

# Handle errors and logging
@Client.on_message(filters.exception)
async def error_handler(client, message, error):
    logging.error(f"Error in chat {message.chat.id}: {error}")
    await message.reply_text(f"Oops, something went wrong! Please try again later.")

