import os
from pyrogram import Client, filters
import yt_dlp

@Client.on_message(filters.regex(r"https?://(?:www\.)?youtu.be\?v=(\w+)"))
async def download_video(client, message):
   link = message.text

   try:
       # Download the video using yt-dlp
       ydl_opts = {
           "outtmpl": "video.mp4",  # Output filename
           "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"  # Preferred format
       }
       with yt_dlp.YoutubeDL(ydl_opts) as ydl:
           info_dict = ydl.extract_info(link, download=True)

       # Send the downloaded video as a video message
       with open("video.mp4", "rb") as video_file:
           await client.send_video(message.chat.id, video_file)

       # Remove the downloaded file
       os.remove("video.mp4")

       await message.reply_text("Video sent!")
   except Exception as e:
       await message.reply_text(f"Error downloading video: {e}")
