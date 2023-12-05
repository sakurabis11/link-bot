import re
from pyrogram import Client, filters
from pyrogram.types import *
import os
import requests
import base64
from shazamio import Shazam
from deezer import Session

# Define your client id and client secret
client_id = "d3a0f15a75014999945b5628dca40d0a"
client_secret = "e39d1705e35c47e6a0baf50ff3bb587f"

# Encode the client id and client secret
credentials = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

# Define a function to get the access token
def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    try:
        return response.json()["access_token"]
    except KeyError:
        print(f"Error fetching access token: {response.text}")
        return None

async def download_deezer(url):
    try:
        # Use `deezer` library to download the song
        
        session = Session()
        song = session.song(url)
        song.download()
        return song.path
    except Exception as e:
        print(f"Error downloading from Deezer: {e}")
        return None

async def download_shazam(query):
    try:
        shazam = shazam.Shazam()
        song = shazam.recognize(query)
        # Identify the song provider and download accordingly
        if song.provider == "deezer":
            return await download_deezer(song.url)
        else:
            print(f"Unsupported provider: {song.provider}")
            return None
    except Exception as e:
        print(f"Error identifying or downloading from Shazam: {e}")
        return None

@Client.on_message(filters.command("spotify"))
async def spotify(client, message):
    # Get the access token
    access_token = get_access_token()
    if not access_token:
        await message.reply_text("Failed to get Spotify access token.")
        return

    # Get the song name or Spotify URL from the command
    song_name_or_url = message.command[1:]
    song_name_or_url = " ".join(song_name_or_url)

    # Check if the command argument is a Spotify URL
    match = re.match(r"https://open\.spotify\.com/track/([a-zA-Z0-9]+)", song_name_or_url)
    if match:
        # If it is a Spotify URL, extract the song ID from the URL
        song_id = match.group(1)
    else:
        # If it is not a Spotify URL, search for the song on Spotify
        song_name = song_name_or_url
        url = f"https://api.spotify.com/v1/search?q={song_name}&type=album,track"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        try:
            data = response.json()
        except JSONDecodeError:
            print(f"Error parsing Spotify search response: {response.text}")
            return

        item = data["tracks"]["items"][0]
        song_id = item["id"]

    # Get the song thumbnail and details from Spotify
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
    except JSONDecodeError:
        print(f"Error fetching song details: {response.text}")
        return

    # Get the song thumbnail
    thumbnail_url = data["album"]["images"][0]["url"]

    # Get the song details
    artist = data["artists"][0]["name"]
    name = data["name"]
    album = data["album"]["name"]
    release_date = data["album"]["release_date"]

    # Check for platform and download the song if possible
    if re.match(r"https://deezer\.com/", song_name_or_url):
        downloaded_song_path = await download_deezer(song_name_or_url)
    else:
        # Use Shazam to identify the song and download it from a suitable source
        downloaded_song_path = await download_shazam(song_name_or_url)

    # Send the downloaded song or appropriate message
    if downloaded_song_path:
        await message.reply_document(document=downloaded_song_path)
    else:
        await message.reply_text(
            f"Couldn't download the song. Please try a different URL or search term."
        )

