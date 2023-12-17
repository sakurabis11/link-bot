import os
import logging
import re
from pyrogram import Client, filters
from youtube_dl import YoutubeDL

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define file path for temporary downloads
DOWNLOAD_DIR = "downloads"

# Download options for youtube-dl
ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
}


@Client.on_message(filters.command("download"))
async def handle_download(client, message):
    # Extract YouTube link from the message
    link = message.text.split()[1]

    # Check if it's a video or playlist link
    is_playlist = bool(re.search("^https://www.youtube.com/playlist", link))

    try:
        # Download song(s) using youtube-dl
        with YoutubeDL(ydl_opts) as ydl:
            if is_playlist:
                playlist_info = ydl.extract_info(link, download=False)
                for entry in playlist_info["entries"]:
                    await download_and_send_song(client, message, entry["id"])
            else:
                song_info = ydl.extract_info(link, download=False)
                await download_and_send_song(client, message, song_info["id"])
    except Exception as e:
        logging.error(f"Error downloading song: {e}")
        await message.reply_text(f"Error downloading song: {e}")


async def download_and_send_song(client, message, video_id):
    # Download and extract audio
    try:
        ydl_opts["outtmpl"] = f"{DOWNLOAD_DIR}/{video_id}.%(ext)s"
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
        audio_path = f"{DOWNLOAD_DIR}/{video_id}.mp3"

        # Send audio file to chat
        await client.send_audio(message.chat.id, audio_path, caption=f"Here's your song!")

        # Clean up downloaded file
        os.remove(audio_path)
    except Exception as e:
        logging.error(f"Error sending song: {e}")
        await message.reply_text(f"Error sending song: {e}")

