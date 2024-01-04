from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import re

ydl_opts = {
    "format": 'bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/best[height<=?720][ext=mp4]/best',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'
    }],
}

regex = r"^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(?:watch\?v=|embed/|v/|.+\?v=)?([^&=\n%\?]{11})"

@Client.on_message(filters.regex(regex))
async def download_video(client, message):
    text = message.text

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=False)
            video_filename = f"{info['title']}.mp4"

            # Download the video
            ydl.download([text])  # No need to specify output_filename here

            # Send the downloaded video as a video message
            client.send_video(  # Use client.send_video to send the video file
                message.chat.id,
                video_filename,
                caption=info.get("title", "YouTube Video"),
                thumb=info.get("thumbnail", ""),
            )
    except Exception as e:
        await message.reply_text(f"Error downloading video: {e}")
