import asyncio
import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

@Client.on_message(filters.command("song"))
async def song(client, message):
    # Get the song name from the message
    song_name = message.text.split(" ")[1]

    # Download the song using yt-dlp
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                # Extract the audio data from the video
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{song_name}"])

    # Get the downloaded song file path
    downloaded_file = os.path.join(os.getcwd(), f"{song_name}.mp3")

    # Send the song as an audio message
    await client.send_audio(message.chat.id, downloaded_file)
