import re
from pyrogram import Client, filters
from pyrogram.types import *
import os
import requests
import base64
import deezer
from mutagen import mp3
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Ignore this add the value to the info.py
client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET

# Encode the client id and client secret
credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')

# Define a function to get the access token
def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']

# Define a function to download the song
def download_song(track_id):
    # Create a Deezer session
    session = deezer.Session()

    # Get the song information
    song = session.get_track(track_id)

    # Check if the song is available
    if not song.is_available:
        return None

    # Get the song download URL
    download_url = session.get_download_url(song)

    # Download the song
    response = requests.get(download_url)

    # Check for successful download
    if response.status_code == 200:
        # Save the song to a temporary file
        with open(f"temp_song_{track_id}.mp3", "wb") as f:
            f.write(response.content)

        # Add ID3 tags to the song
        metadata = mp3.MP3(f"temp_song_{track_id}.mp3")
        metadata["title"] = song.title
        metadata["artist"] = song.artist.name
        metadata.save()

        # Send the downloaded song to the user
        await message.reply_audio(audio=f"temp_song_{track_id}.mp3", caption=f"Downloading {song.title} completed!")

        # Delete the temporary file
        os.remove(f"temp_song_{track_id}.mp3")
    else:
        await message.reply_text(f"Error downloading the song. Please try again later.")

@Client.on_message(filters.command("spotify"))
async def spotify(client, message):
    # Get the access token
    access_token = get_access_token()

    # Get the song name or Spotify URL from the command
    song_name_or_url = message.command[1:]
    song_name_or_url = " ".join(song_name_or_url)

    # Check if the command argument is a Spotify URL
    match = re.match(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)', song_name_or_url)
    if match:
        # If it is a Spotify URL, extract the song ID from the URL
        song_id = match.group(1)
    else:
        # If it is not a Spotify URL, search for the song on Spotify
        song_name = song_name_or_url
        url = f'https://api.spotify.com/v1/search?q={song_name}&type=album,track'
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        # Get the first search result
        item = data["tracks"]["items"][0]

        # Get the song ID
        song_id = item["id"]

    # Get the song thumbnail and details from Spotify
    url = f'https://api.spotify.com/v1/tracks/{song_id}'
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the song thumbnail
    thumbnail_url = data["album"]["images"][0]["url"]

    # Get the song details
    artist = data["artists"][0]["name"]
    name = data["name"]
    album = data["album"]["name"]
    release_date = data["album"]["release_date"]

    # Send the song thumbnail and details to the user
    await message.reply_photo(photo=thumbnail_url, caption=f"ᴛɪᴛʟᴇ: <code>{name}</code>\nᴀʀᴛɪsᴛ: <code>{artist}</code>\nᴀʟʙᴜᴍ: <code>{album}</code>\nʀᴇʟᴇᴀsᴇ ᴅᴀᴛᴇ: <code>{release_date}</code>\n")
