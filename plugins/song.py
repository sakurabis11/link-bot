import asyncio
import os
import re
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch
from thumbnail import download_thumbnail


@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    # Check if user sent song name
    if len(message.text.split()) < 2:
        await message.reply("Please provide the song name you want to download")
        return

    # Extract song name
    song_name = message.text.split()[1:]
    song_name = " ".join(song_name)

    # Show processing emoji
    await message.reply(" Searching for your song...")

    # Search for song
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]

    # Download thumbnail
    thumbnail_filename = f"{song_title}.jpg"
    try:
        await download_thumbnail(f"https://www.youtube.com{song_url}", thumbnail_filename)
    except Exception as e:
        await message.reply(f"Error downloading thumbnail: {e}")
        return

    # Download song
    yt = YouTube(f"https://www.youtube.com{song_url}")
    audio_streams = yt.streams.filter(only_audio=True)

    if not audio_streams:
        await message.reply("No audio stream found for the specified video")
        return

    video = audio_streams.first()
    audio_filename = f"{song_title}.mp3"

    try:
        # Download song
        video.download(filename=audio_filename)

        # Get duration
        duration = str(datetime.timedelta(seconds=int(video.duration)))

        # Send caption with info and thumbnail
        caption = f""" **Downloaded:** {song_title}.mp3
        ⏳ **Duration:** {duration}
         **YouTube Link:** https://www.youtube.com{song_url}"""
        await message.reply_audio(audio_filename, caption=caption, photo=thumbnail_filename)

        # Delete downloaded files
        os.remove(audio_filename)
        os.remove(thumbnail_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")

