from pyrogram import Client, filters
import yt_dlp
import re
import requests

regex = r"^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(?:watch\?v=|embed/|v/|.+\?v=)?([^&=\n%\?]{11})"

@Client.on_message(filters.regex(regex))
async def download_video(client, message):
    try:
        url = message.text  # Indent this line correctly

        ydl_opts = {
            'outtmpl': '%(id)s.%(ext)s',
            'quiet': True,
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'logtostderr': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            video_id = info['id']
            video_title = info['title']
            video_thumbnail = info['thumbnail']
            video_duration = info['duration']
            video_url = info['url']
            video_ext = info['ext']
            video_format = info['format'].split('/')[1].split('+')[0].split(';')[0].split('?')[0]

            # Download the video
            with ydl:
                ydl.download([url])

            # Send the downloaded video
            video_file = f"{video_id}.{video_ext}"  # Construct the filename
            await message.reply_video(video_file)

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")




