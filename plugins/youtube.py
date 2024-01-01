import pyrogram
from pyrogram import Client, filters
import yt_dlp

@Client.on_message(filters.regex(r"https?://(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-_]*)(&(amp;)?[\w\?=]*)?"))
async def download_video(client, message):
    try:
        url = message.text

        with yt_dlp.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'}) as ydl:
            ydl.download([url])

        video_file = ydl.extract_info(url, download=False)['title'] + ".mp4"  # Get filename

        await message.reply_video(video_file)

    except Exception as e:
        await message.reply_text(f"Error downloading video: {e}")

