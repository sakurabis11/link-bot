# Import the necessary modules
from pyrogram import Client, filters
import requests
import re

# Define a handler for messages that match the Spotify URL pattern
@Client.on_message(filters.regex(r'https://open.spotify.com/track/.*'))
async def handle_spotify_link(bot, msg):
    # Extract the Spotify URL from the message text
    spotify_link = msg.text

    # Use an API to download the song from the Spotify link
    api_response = requests.get(f"https://api.spotifydl.net/convert?url={spotify_link}")

    # If the song was downloaded successfully
    if api_response.status_code == 200:
        # Send the downloaded song to the user
        await bot.send_audio(
            chat_id=msg.chat.id,
            audio=api_response.content,
            caption="Here's the song you requested!"
        )
    else:
        # If there was an error, notify the user
        await bot.send_message(
            chat_id=msg.chat.id,
            text="Apologies, I was unable to download the song. Please try again later."
        )
