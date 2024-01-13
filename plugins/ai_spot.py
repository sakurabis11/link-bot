
import asyncio
import re
import requests
from pyrogram import Client, filters
from bs4 import BeautifulSoup
from pyrogram import types

# Define the regex pattern for Spotify URLs
spotify_url_regex = re.compile(r"https://open.spotify.com/track/([a-zA-Z0-9]+)")

# Define the download function
async def download_song(url):
    # Extract the song ID from the URL
    song_id = spotify_url_regex.match(url).group(1)

    # Send a request to the Spotify API to get the song metadata
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer BQB_royu_irt_M1tl-5amY3DSl29-lC82rPMF9Piq0tK8b3vXacMk9s9nol57Df04PQd8_w23O2Gay3inag'
    }
    response = requests.get(f"https://api.spotify.com/v1/tracks/{song_id}", headers=headers)

    # Parse the song metadata from the response
    song_data = response.json()
    song_name = song_data['name']
    artist_name = song_data['artists'][0]['name']

    # Download the song file
    download_url = song_data['preview_url']
    song_file = requests.get(download_url)

    # Save the song file to disk
    with open(f"{song_name}-{artist_name}.mp3", "wb") as f:
        f.write(song_file.content)

    # Return the song file path
    return f"{song_name}-{artist_name}.mp3"


# Define the Telegram bot event handler
@Client.on_message(filters.regex(spotify_url_regex))
async def handle_spotify_url(client: Client, message: types.Message):
    # Extract the Spotify URL from the message
    spotify_url = message.text

    # Send a message to the user indicating that the download is in progress
    loading_message = await message.reply_text("Downloading song...")

    # Download the song file
    song_file_path = await download_song(spotify_url)

    # Send the downloaded song file to the user
    await client.send_audio(
        message.chat.id,
        audio=song_file_path,
        caption=f"{song_file_path.split('/')[-1]}",
        reply_to_message_id=message.message_id
    )

    # Delete the downloaded song file from disk
    os.remove(song_file_path)

    # Delete the loading message
    await loading_message.delete()


