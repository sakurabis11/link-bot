import asyncio
import os
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, 
from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL
from random import randint
import shutil


DOWNLOAD_DIRECTORY = "downloads"

@Client.on_message(filters.command("download"))
async def download_music(client, message):
    if not os.path.exists(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)

    song_name = message.text.split(" ")[1]

    try:
        with YoutubeDL({'format': 'best'}) as ydl:
            video_info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            video_url = video_info['entries'][0]['url']
            video_title = video_info['entries'][0]['title']

            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Download", callback_data=f"download:{video_url}")]])
            await message.reply("Song found:", reply_markup=keyboard)
    except Exception as e:
        await message.reply(f"Error: {e}")

@Client.on_callback_query(filters.callback_data.startswith("download:"))
async def download_song(client, callback_query):
    video_url = callback_query.data.split(":")[1]
    song_title = video_url.split("/")[-1].split(".")[0]

    try:
        with YoutubeDL({'format': 'best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}) as ydl:
            ydl.download([video_url])

        await callback_query.edit_message_text(f"Song downloaded: {song_title}.mp3")
    except Exception as e:
        await callback_query.edit_message_text(f"Error downloading song: {e}")
