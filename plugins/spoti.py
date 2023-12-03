import re
from pyrogram import Client, filters
from pyrogram.types import *
import os
import requests
import base64
import pytube

# Define your client id and client secret
CLIENT_ID = "d3a0f15a75014999945b5628dca40d0a"
CLIENT_SECRET = "e39d1705e35c47e6a0baf50ff3bb587f"

# Encode the client id and client secret
CREDENTIALS = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")).decode("utf-8")


async def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {CREDENTIALS}", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

@Client.on_message(filters.command("spotify"))
async def spotify(client, message):
    # Get the song name
    song_name = message.text.split(" ")[1]
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

async def search_and_get_song_id(song_name, access_token):
    url = f"https://api.spotify.com/v1/search?q={song_name}&type=album,track"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the first search result
    item = data["tracks"]["items"][0]

    # Get the song ID
    song_id = item["id"]

    return song_id


async def get_song_data(song_id, access_token):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the song thumbnail and details
    thumbnail_url = data["album"]["images"][0]["url"]
    artist = data["artists"][0]["name"]
    name = data["name"]
    duration_ms = data["duration_ms"]
    duration = str(int(duration_ms / 1000)) + " seconds"
    album = data["album"]["name"]
    release_date = data["album"]["release_date"]
    popularity = data["popularity"]

    return thumbnail_url, artist, name, duration, album, release_date, popularity

    # Get the access token and song information
    access_token = await get_access_token()
    song_id = await search_and_get_song_id(song_name, access_token)
    thumbnail_url, artist, name, duration, album, release_date, popularity = await get_song_data(song_id, access_token)

    # Download the song using pytube
    yt = pytube.YouTube(f"https://open.spotify.com/track/{song_id}")
    audio_streams = yt.streams.filter(only_audio=True)
    audio_stream = audio_streams[0]  # Select the first audio stream
    audio_stream.download()

    # Get the downloaded song filename
    downloaded_filename = audio_stream.default_filename

    # Send the song file to the user along with song information
    await message.reply_document(
        document=downloaded_filename, caption=f"**Song:** {name}\n**Artist:** {artist}\n**Album:** {album}\n**Duration:** {duration}\n**Release Date:** {release_date}\n**Popularity:** {popularity}"
    )
