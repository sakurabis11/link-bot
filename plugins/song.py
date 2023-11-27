import asyncio
import os
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch


@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    song_name = message.text.split()[1]

    # Search for the song on YouTube
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]

    # Download the song using pytube
    yt = YouTube(f"https://www.youtube.com{song_url}")
    video = yt.streams.filter(only_audio=True).first()
    audio_filename = f"{song_title}.mp3"

    try:
        video.download(filename=audio_filename)
        await message.reply(f"Song downloaded: {audio_filename}")

        # Send the downloaded song to the user
        await message.reply_audio(audio_filename)

        # Delete the downloaded song after sending it
        os.remove(audio_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")

