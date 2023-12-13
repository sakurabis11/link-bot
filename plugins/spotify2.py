from pyrogram import Client, filters
from spotipy import Spotify
from yt_dlp import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Replace with your Spotify credentials
CLIENT_ID = SPOTIFY_CLIENT_ID
CLIENT_SECRET = SPOTIFY_CLIENT_SECRET

# Spotify and Youtube-DL instances
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}


@Client.on_message(filters.command("spotifyin"))
async def download_song(client, message):
    song_url = message.text.split(" ")[1]
    try:
        track = sp.track(song_url)
        name = track["name"]
        artist = track["artists"][0]["name"]
        yt_url = sp.track_to_youtube_url(song_url)

        # Download song using yt-dl
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(yt_url, download=True)

        # Send downloaded file to user
        file = open(f"{name}-{artist}.mp3", "rb")
        client.send_document(message.chat.id, file)
        file.close()
        message.reply_text(f"Downloaded song: {name} by {artist} ")
    except Exception as e:
        message.reply_text(f"Error downloading song: {e}")

