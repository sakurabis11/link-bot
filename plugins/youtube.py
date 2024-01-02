import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import re
from yt_dlp import YoutubeDL

ydl_opts = {
    "format": "bestvideo[height<=720]+bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "extract_audio": True,
    "add_thumbnail": True,
}

@Client.on_message(filters.regex(r"https?://(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-_]*)(&(amp;)?[\w\?=]*)?"))
async def download_video(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        video_url = message.text
        
        with YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_url, download=False)
            video_title = video_info["title"]

            try:
                await message.reply_text(f"Downloading '{video_title}'...")
                ydl.download([video_url])
                
                # Send video file and thumbnail
                video_file = f"{video_info['id']}.mp4"
                thumbnail_file = f"{video_info['id']}.jpg"
                await message.reply_video(open(video_file, "rb"),
                                         caption=f"Downloaded: {video_title}",
                                         thumbnail=open(thumbnail_file, "rb"))
                
                # Delete downloaded files
                os.remove(video_file)
                os.remove(thumbnail_file)
            except FloodWait as e:
                await asyncio.sleep(e.ttl)
                await message.reply_text(f"Please try again later.")
            except Exception as e:
                await message.reply_text(f"Error: {e}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

