import asyncio
import os
import re
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch


@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    song_name = message.text

    if not song_name:
        await client.send_message(message.chat.id, "Please provide a song name to search. Usage: /song (song_name) or (song_name + Artist_name)")
        return

    # Search for the song on YouTube
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]

    # Download the song using pytube
    yt = YouTube(f"https://www.youtube.com{song_url}")
    audio_streams = yt.streams.filter(only_audio=True)

    if not audio_streams:
        await client.send_message(message.chat.id, "No audio stream found for the specified video")
        return

    video = audio_streams.first()
    audio_filename = f"{song_title}.mp3"

    try:
        video.download(filename=audio_filename)
        await message.reply(f"**Song downloaded: {audio_filename}**")

        # Send the downloaded song to the user
        await message.reply_audio(audio_filename)

        # Delete the downloaded song after sending it
        os.remove(audio_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")
