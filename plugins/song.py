import asyncio
import os
import re
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch


@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    # Check if user provided song name
    if len(message.text.split()) < 2:
        await message.reply("Please provide song name you want to download")
        return

    song_name = message.text.split()[1:]  # Extract song name
    song_name = " ".join(song_name)  # Combine parts

    # Search for song on YouTube
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]

    # Send hourglass emoji before searching
    await message.reply(f"⏳ Searching for your song... Please wait!")

    # Download song using pytube
    yt = YouTube(f"https://www.youtube.com{song_url}")
    audio_streams = yt.streams.filter(only_audio=True)

    if not audio_streams:
        await client.send_message(message.chat.id, "No audio stream found for the specified video")
        return

    video = audio_streams.first()
    audio_filename = f"{song_title}.mp3"

    try:
        # Download song
        video.download(filename=audio_filename)

        # Wait for 6 seconds before removing emoji
        await asyncio.sleep(6)
        await message.edit_text(None)

        # New message for song details - avoids editing issue
        new_message = client.send_message(
            message.chat.id,
            f"**Downloaded: {song_title}**\n⏱️ Duration: {int(video.duration / 60)}:{int(video.duration % 60)} minutes\n YouTube Link: https://www.youtube.com{song_url}",
        )

        # Send downloaded song with new message
        await new_message.reply_audio(audio_filename)

        # Delete downloaded song afterwards
        os.remove(audio_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")

