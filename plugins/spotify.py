import asyncio
import base64
import requests
from pyrogram import Client, filters
from spotipy import Spotify
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Create Spotify OAuth object
sp_oauth = SpotifyOAuth(
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)

# Create Spotify client instance
spotify = Spotify(auth_manager=sp_oauth)

# Create Spotify downloader instance
sp_downloader = SpotifyDownloader(spotify=spotify)

# Handle /spotify command
@Client.on_message(filters.command("spotify"))
async def download_song(client, message):
    try:
        # Extract song name from command
        song_name = message.text.split(" ")[1]

        # Search for song on Spotify
        search_results = spotify.search(q=song_name, type="track")

        # Check if song was found
        if not search_results["tracks"]["items"]:
            await message.reply_text("Song not found")
            return

        # Get song details
        song = search_results["tracks"]["items"][0]
        song_id = song["id"]
        song_name = song["name"]
        artist = song["artists"][0]["name"]
        album_name = song["album"]["name"]
        album_image_url = song["album"]["images"][0]["url"]

        # Download song from Spotify
        audio_data = sp_downloader.download_track(song_id)
        audio_filename = f"{song_name}.mp3"

        # Send song details and thumbnail
        await message.send_photo(
            photo=album_image_url,
            caption=f"**Song:** {song_name}\n**Artist:** {artist}\n**Album:** {album_name}",
        )

        # Upload song to Telegram
        await message.reply_audio(
            audio=audio_data,
            filename=audio_filename,
            caption=f"**Song:** {song_name}",
        )
    except Exception as e:
        await message.reply_text(f"Error: {e}")
