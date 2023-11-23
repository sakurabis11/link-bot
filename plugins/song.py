import pyrogram
import asyncio
from pyrogram import Client, filters, enums
from youtube_dl import YoutubeDL
import requests

@Client.on_message(filters.command("download"))
async def download_song(client, message):
    try:
        song_name = message.text.split(" ")[1]
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        }
        with YoutubeDL(ydl_opts) as ydl:
            song_info = ydl.extract_info(song_name, download=False)
            song_url = song_info["entries"][0]["url"]
            await message.reply_text(f"Downloading {song_info['title']}...")
            await message.reply_document(song_url, caption=song_info["title"])
    except Exception as e:
        await message.reply_text(f"Error: {e}")
