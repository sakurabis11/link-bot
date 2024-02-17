
import os
import re
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch

DOWNLOAD_DIRECTORY = os.environ.get("DOWNLOAD_DIRECTORY", "./downloads")


@Client.on_message(filters.regex(r"https://open.spotify.com/track/[a-zA-Z0-9]+"))
async def spotify_track_handler(client: Client, message: Message):
    track_url = message.text
    track_id = track_url.split("/")[-1]
    results = YoutubeSearch(f"{track_id} audio", max_results=1).to_dict()
    if results:
        video_id = results[0]["id"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        await message.reply_text(f"**Title:** {results[0]['title']}\n**Duration:** {results[0]['duration']}\n\n**Downloading...**")
        await client.send_chat_action(message.chat.id, "download")
        file_path = await client.download_media(video_url, file_name=f"{track_id}.mp3", progress=progress_callback)
        if file_path:
            await message.reply_audio(file_path, caption=results[0]["title"], thumb=results[0]["thumbnails"][0])
        else:
            await message.reply_text("Failed to download the song.")
    else:
        await message.reply_text("No results found.")

def progress_callback(current, total):
    print(f"Downloaded {current * 100 / total:.1f}%")


