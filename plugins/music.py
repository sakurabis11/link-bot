import asyncio
import os
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.errors import FloodWait
import ffmpeg
from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL
from random import randint
import shutil
import asyncio
import re

DOWNLOAD_DIRECTORY = "downloads"
callback_data_mapping = {}

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

            # Use a unique identifier for the file name (e.g., video ID)
            video_id = video_info['entries'][0]['id']
            song_title = f"{video_id}.mp3"

            # Shorten the file name to avoid errors
            if len(song_title) > 255:
                song_title = song_title[:255]

            # Use a short identifier as callback data
            callback_data = f"download:{video_id}"
            callback_data_mapping[callback_data] = video_url

            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Download", callback_data=callback_data)]])
            await message.reply("Song found:", reply_markup=keyboard)
    except Exception as e:
        await message.reply(f"Error: {e}")

@Client.on_callback_query(filters.regex(r"download:\w+"))
async def download_song(client, callback_query):
    callback_data = callback_query.data
    video_url = callback_data_mapping.get(callback_data)

    if video_url:
        song_title = f"{callback_data}.mp3"

        try:
            with YoutubeDL({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}) as ydl:
                ydl.download([video_url])

            await callback_query.edit_message_text(f"Song downloaded: {song_title}")

            # Send the audio file after downloading
            await send_audio(client, callback_query.message, song_title)
        except Exception as e:
            await callback_query.edit_message_text(f"Error downloading song: {e}")
    else:
        await callback_query.edit_message_text("Invalid callback data. Please try again.")

async def send_audio(client, message, song_title):
    audio_path = os.path.join(DOWNLOAD_DIRECTORY, song_title)

    if os.path.exists(audio_path):
        try:
            await client.send_audio(message.chat.id, audio_path, reply_to_message_id=message.id)
            await message.reply(f"Audio sent: {song_title}")
            os.remove(audio_path)  # Delete the downloaded audio file after sending it
        except Exception as e:
            await message.reply(f"Error sending audio: {e}")
    else:
        await message.reply("Audio file not found.")
