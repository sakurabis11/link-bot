import asyncio
import os
import pytube
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pyrogram import Client, filters


def get_song_details(spotify_link):
    try:
        # Extract song ID from Spotify link
        song_id = spotify_link.split("/")[-1]

        # Initialize Spotify API with client ID and secret
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="21cf39f58bf7494d8fa377c59b72211c",
                                                       client_secret="cc98f5a4038e40a9adc7573bf5b072a5",
                                                       redirect_uri="http://://localhost:27017"))

        # Get song details using Spotify API
        song_info = sp.track(song_id)
        song_title = song_info["name"]
        song_artist = song_info["artists"][0]["name"]

        return song_title, song_artist

    except Exception as e:
        raise e


def download_song(song_title, song_artist, spotify_link):
    try:
        # Extract song ID from Spotify link
        song_id = spotify_link.split("/")[-1]

        # Initialize YouTube with pytube
        yt = pytube.YouTube(f"https://www.youtube.com/watch?v={song_id}")

        # Check if the video has any streams
        if not yt.streams:
            raise Exception(f"❌ Song unavailable: {song_title} by {song_artist}")

        # Check for copyright restrictions in the song's description
        if "copyright" in yt.description:
            raise Exception(f"❌ Song unavailable due to copyright restrictions: {song_title} by {song_artist}")

        # Download the first available stream of the video
        video = yt.streams.first()
        video.download(filename=f"{song_title}.mp4")

        # Convert MP4 to MP3
        os.system(f"ffmpeg -i {song_title}.mp4 -q:a 0 -b:a 192k {song_title}.mp3")

        # Delete the temporary MP4 file
        os.remove(f"{song_title}.mp4")

        return f"{song_title}.mp3"

    except Exception as e:
        raise e


@Client.on_message(filters.command(["download"]))
async def download_song_handler(client, message):
    if message.chat.id != message.from_user.id:
        return

    if message.reply_to_message is None or message.reply_to_message.text is None:
        await message.reply_text("Please reply to a message containing a Spotify song link.")
        return

    spotify_link = message.reply_to_message.text

    try:
        song_title, song_artist = get_song_details(spotify_link)

        await message.reply_text(f"Downloading: {song_title} by {song_artist}")

        downloaded_file_path = await download_song(song_title, song_artist, spotify_link)

        # Send the downloaded MP3 file to the user
        await message.reply_document(downloaded_file_path)

        # Delete the temporary MP3 file
        os.remove(downloaded_file_path)

        await message.reply_text(f"✅ Song downloaded: {song_title} by {song_artist}")

    except Exception as e:
        if "copyright" in str(e):
            await message.reply_text(f"❌ Song unavailable due to copyright restrictions: {song_title} by {song_artist}")
        else:
            await message.reply_text(f"❌ Error downloading song: {e}")
