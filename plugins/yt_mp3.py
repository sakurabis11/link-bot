import os
import pyrogram
from pyrogram import Client, filters
import yt_dlp

@Client.on_message(filters.command("mp3"))
async def download_song(client, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /mp3 <YouTube video link>")
        return

    youtube_link = message.command[1]

    try:
        # Download audio using yt-dlp
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": "%(title)s.%(ext)s",
            "progress_hooks": [
                lambda d: message.reply_text(f"Downloading {d['filename']}..."),
                lambda d: message.reply_text(f"Download complete!"),
            ]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_link])

        # Send downloaded audio file
        audio_file = os.path.abspath(ydl.extract_info(youtube_link, download=False)['title'] + ".mp3")
        await message.reply_audio(audio_file)

        os.remove(audio_file)  # Remove the downloaded audio file

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")


