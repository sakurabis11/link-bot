import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
import ffmpeg
from youtube_dl import YoutubeDL
from random import randint
import shutil
import re

import os
import pyrogram
from pyrogram import filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL

# Define the download function
def download_song(message: Message):
    # Extract the song name from the message
    song_name = message.text.split(" ")[1]

    # Download the song using youtube-dl
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }],
        "output": f"songs/{song_name}.mp3"
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{song_name}"])

    # Send a download completion message
    message.reply(f"Song downloaded: {song_name}.mp3")

# Add the download command handler
@Client.on_message(filters.text & filters.command(["download"]))
async def download_command_handler(bot: pyrogram.Client, message: Message):
    # Check if the song name is provided
    if len(message.text.split(" ")) < 2:
        message.reply("Please provide the song name to download.")
        return

    # Start the download process
    download_song(message)
