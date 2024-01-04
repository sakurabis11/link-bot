import asyncio
import os
import re
import mutagen  

from pyrogram import Client, filters
from pytube import YouTube
from info import REQUESTED_CHANNEL
from youtube_search import YoutubeSearch

@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    # Check for song name in command
    if len(message.text.split()) < 2:
        await message.reply("Please provide the song name you want. Example: /song lover")
        return

    song_name = " ".join(message.text.split()[1:])  # Extract song name

    await message.reply("Searching...")  # Send searching message

    # Search for the song on YouTube
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    if not search_results:
        await message.reply("No song found with that name.")
        return

    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]
    duration = search_results[0]["duration"]  # Extract duration for potential use
    thumbnail_url = search_results[0]["thumbnails"][0]["url"]

    # Download the song using pytube
    yt = YouTube(f"https://www.youtube.com{song_url}")
    audio_streams = yt.streams.filter(only_audio=True)
    if not audio_streams:
        await message.reply("No audio stream found for the specified video.")
        return

    video = audio_streams.first()
    audio_filename = f"{song_title}.mp3"

    try:
        video.download(filename=audio_filename)

        # Embed thumbnail into audio file
        audio = mutagen.File(audio_filename)
        audio.add_tags()  # Create tags if they don't exist
        audio["artwork"] = open(thumbnail_url, "rb").read()
        audio.save()

        # Prepare audio caption (incorporate duration if needed)
        song_caption = f"** {song_title}**\n Duration: {duration}\n"  # Include duration

        # Send audio with embedded thumbnail
        await message.reply_audio(
            audio_filename,
            caption=song_caption,
            thumb=thumbnail_url  # Use 'thumb' parameter for embedded thumbnail
        )

        await client.send_message(REQUESTED_CHANNEL, text=f"#song\nRequested from {message.from_user.mention}\nRequest is {song_name}")

        # Delete the downloaded song after sending
        os.remove(audio_filename)

    except Exception as e:
        # Consider more specific error handling if needed
        await message.reply(f"An error occurred during song download: {e}")
