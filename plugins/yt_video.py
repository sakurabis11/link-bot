from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
import asyncio
import os
from yt_dlp import YoutubeDL

def get_text(message: Message) -> str:
    text = message.text.strip()
    if not text or " " not in text:
        return ""
    return text.split(None, 1)[1]

@Client.on_message(filters.command("video"))
async def download_video(client: Client, message: Message):
 try:
    text = get_text(message)  

    if not text:
        await message.reply_text("Invalid command syntax! Use /video or /mp4 followed by the video title or URL.")
        return

    async with client.conversation(message.chat.id) as chat:
        await chat.send_message("**Searching for your video...**")

        search = YoutubeSearch(text, max_results=1).to_dict()  
        if not search:
            await chat.send_message("Sorry, couldn't find any videos matching your query.")
            return

        video_url = search[0]["link"]
        video_title = search[0]["title"]

        # Download thumbnail using YoutubeDL (more reliable)
        ydl_opts = {"format": "best", "skip_download": True}
        with YoutubeDL(ydl_opts) as ytdl:
            info = ytdl.extract_info(video_url, download=False)
            thumbnail_url = info.get("thumbnail", "")

        await chat.send_photo(thumbnail_url, caption=f"**Title:** {video_title}")

        # Download the video
        download_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio/best[ext=m4a]/best",
            "merge_output_format": "mp4",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "aac",
                "preferredquality": "192",
            }],
            "outtmpl": "%(id)s.%(ext)s",
            "quiet": True,
        }

        try:
            with YoutubeDL(download_opts) as ytdl:
                ytdl.download([video_url])
        except Exception as e:
            await chat.send_message(f"Download failed: {str(e)}")
            return

        file_path = f"{ytdl.prepare_filename(info)}"  # Use prepared filename

        await chat.send_video(
            video=open(file_path, "rb"),
            caption=f"**Requested by:** {message.from_user.mention}",
            supports_streaming=True,
            reply_to_message_id=message.id,
        )

        # Cleanup (can be improved for better error handling)
        os.remove(file_path)

 except Exception as e:
        await message.reply_text(f"{e}")


