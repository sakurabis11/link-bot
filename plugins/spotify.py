import re
from pyrogram import Client, filters
from pyrogram.types import *
import os
import requests
import base64
from spotdl import SpotifyOAuth
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from spotipy import Spotify

# Replace with your Spotify API credentials
spotify_client_id = SPOTIFY_CLIENT_ID
spotify_client_secret = SPOTIFY_CLIENT_SECRET

# Configure your preferred yt-dlp options
ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}

# Create Pyrogram client and Spotify objects
spotify_api = Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret))
spotify_downloader = SpotifyDownloader(spotify_api)

@Client.on_message(filters.command("spotify"))
async def process_message(client, message):
        song_name = message.content.split()[1]
    
        # Try searching for song on Spotify
        try:
            song = spotify_api.search(q=song_name, type="track", limit=1)["tracks"]["items"][0]
        except Exception as e:
            await message.reply_text(f"Error searching for song: {e}")
            return

        # Send song details and thumbnail
        await message.reply_photo(song["album"]["images"][0]["url"])
        await message.reply_text(f"Title: {song['name']}\nArtist: {song['artists'][0]['name']}")

        # Download song from YouTube Music
        try:
            filename = await spotify_downloader.download_track(song["uri"], filename_template="%(title)s.%(ext)s")
        except Exception as e:
            await message.reply_text(f"Error downloading song: {e}")
            return

        # Upload downloaded song with thumbnail
        await message.reply_audio(filename, caption=f"{song['name']} by {song['artists'][0]['name']}")
        os.remove(filename) # Delete downloaded file after uploading
