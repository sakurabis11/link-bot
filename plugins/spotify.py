import re
from pyrogram import Client, filters
from pyrogram.types import *
import os
import requests
import base64
from deezer import Deezer
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET
credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')

# Define functions to handle Spotify and Deezer
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

def get_deezer_track_url(access_token, song_name_or_url):
    match = re.match(r'https://deezer.com/track/([0-9]+)', song_name_or_url)
    if match:
        track_id = match.group(1)
    else:
        search_url = f"https://api.deezer.com/v1/search?q={song_name_or_url}"
        headers = {"Authorization": f"Bearer {access_token}" if access_token else None}
        response = requests.get(search_url, headers=headers)
        data = response.json()
        try:
            track_id = data["tracks"]["data"][0]["id"]
            thumbnail_url = data["tracks"]["data"][0]["album"]["cover_medium"]
            song_details = f"Artist: {data['tracks']['data'][0]['artist']['name']}\nAlbum: {data['tracks']['data'][0]['album']['title']}"
        except:
            return None, None, None
    return f"https://api.deezer.com/v1/track/{track_id}/download", thumbnail_url, song_details

# Deezer Downloader
def download_song_deezer(song_url):
    # Use deezer-py library to download

    client = Deezer()
    song = client.get_track(song_url)
    filename = f"{song.title}.mp3"
    with open(filename, "wb") as f:
        f.write(song.download_link(quality=Deezer.QUALITY_MP3))
    return filename

@Client.on_message(filters.command("spotify") | filters.command("deezer"))
async def download_music(client, message):
    # Get the command
    command, *args = message.command
    song_name_or_url = " ".join(args)

    # Check for Spotify or Deezer command
    if command == "spotify":
        access_token = get_access_token()
        song_url, thumbnail_url, song_details = get_deezer_track_url(access_token, song_name_or_url)
    elif command == "deezer":
        song_url, thumbnail_url, song_details = get_deezer_track_url(None, song_name_or_url)

    # Download the song
    if song_url:
        downloaded_song_path = download_song_deezer(song_url)
        if downloaded_song_path:
            # Prepare the data for sending
            media = [
                InputMediaAudio(media=open(downloaded_song_path, "rb")),
                InputMediaPhoto(media=thumbnail_url),
                InputMediaDocument(media=song_details)
            ]

            # Send the audio file, thumbnail and song details
            await client.send_media_group(
                chat_id=message.chat.id,
                media=media
            )
            os.remove(downloaded_song_path)
        else:
            await message.reply_text("Song not found")
    else:
        await message.reply_text("Invalid command or song not found")
