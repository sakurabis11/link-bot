import asyncio
import os
import re
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch

processing_emoji = "⏳"


@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    # Check if the user has provided a song name
    if len(message.text.split()) < 2:
        await message.reply("Please provide the song name you want to download")
        return

    song_name = message.text.split()[1:]  # Extract the song name from the message
    song_name = " ".join(song_name)  # Combine the song name parts into a single string

    # Send processing emoji and delete it later
    await message.reply(processing_emoji)
    await asyncio.sleep(1)
    await message.delete()

    # Search for the song on YouTube
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]

    # Download the song using pytube
    yt = YouTube(f"https://www.youtube.com{song_url}")
    audio_streams = yt.streams.filter(only_audio=True)

    if not audio_streams:
        await client.send_message(
            message.chat.id, "No audio stream found for the specified video"
        )
        return

    video = audio_streams.first()
    audio_filename = f"{song_title}.mp3"

    try:
        # Download the song
        video.download(filename=audio_filename)

        # Extract thumbnail and video duration
        thumb_url = yt.thumbnails[-1].url
        duration = str(yt.length / 60)[:4]  # Convert seconds to minutes:seconds format

        # Send song details and thumbnail
        caption = f"""**Song downloaded: {song_title}**

File Name: {audio_filename}
Duration: {duration} mins
YouTube Link: https://www.youtube.com{song_url}

Enjoy! """
        await message.reply_photo(thumb_url, caption)

        # Send the downloaded song
        await message.reply_audio(audio_filename)

        # Delete the downloaded song after sending it
        os.remove(audio_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")

