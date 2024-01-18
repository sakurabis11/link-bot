import asyncio
import os
from pyrogram import Client, filters
from pytube import YouTube
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

@Client.on_message(filters.command("song"))
async def song_handler(client, message):
    # Get the song name from the message
    song_name = message.text.split(" ")[1]

    # Search for the song on YouTube
    results = YoutubeSearch(song_name, max_results=1).to_dict()

    # Get the video ID of the first result
    video_id = results[0]["id"]

    # Download the song using pytube
    yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download()

    # Convert the audio file to MP3 using yt-dlp
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=" + video_id])

    # Send the MP3 file to the user
    await client.send_audio(message.chat.id, "song.mp3")

    # Delete the downloaded files
    os.remove("song.mp3")


