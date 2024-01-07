from pyrogram import filters, Client
from pyrogram.types import Message
import yt_dlp
import os
import re


@Client.on_message(filters.regex(r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(?:watch\?v=|embed/|v/|.+\?v=)?([^&=\n%\?]{11})"))
async def ytaudio(client, message: Message):
    url = message.text.split(" ", 1)[1]

    try:

        with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': '%(id)s.%(ext)s'}) as ydl:
            info = ydl.extract_info(url, download=False)

            video_title = info.get('title', 'Unknown Title')
            duration = info.get('duration', 'Unknown Duration')
            video_id = info.get('id', 'Unknown ID')
            thumbnail_url = info.get('thumbnail', None)

            if thumbnail_url:
                thumbnail_file = f"{video_id}.jpg"
                ydl.download([url])
            else:
                thumbnail_file = None

            await message.reply_audio(
                audio=f"{video_id}.mp3",
                caption=f"**{video_title}**\nDuration: {duration}\nLink: {youtube_link}",
                thumb=thumbnail_file
            )

            if thumbnail_file:
                os.remove(thumbnail_file)
            os.remove(f"{video_id}.mp3")

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
