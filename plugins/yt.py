from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_dl import YoutubeDL
import yt-dl
import ffmpeg

# Function to download a single song from YouTube URL
def download_song(url, format="bestaudio/best", chat_id=None):
    ydl_opts = {
        "format": format,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info["title"]
        filename = f"{title}.mp3"
        ydl.download([url])
        send_file(chat_id, filename)

# Function to download a playlist from YouTube URL
def download_playlist(url, chat_id=None):
    ydl_opts = {"format": "bestaudio/best"}
    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(url, download=False)
        entries = playlist_info["entries"]
        for entry in entries:
            download_song(entry["url"], chat_id=chat_id)

# Send file function to send downloaded song
def send_file(chat_id, filename):
    bot.send_document(chat_id, document=filename)


# Define command handlers
@Client.on_message(filters.command("download"))
async def handle_download(client: Client, message: Message):
    if len(message.text.split()) < 2:
        client.send_message(message.chat.id, "Please provide a YouTube URL or playlist link.")
        return
    url = message.text.split()[1]
    download_song(url, chat_id=message.chat.id)

@Client.on_message(filters.command("playlist"))
async def handle_playlist(client: Client, message: Message):
    if len(message.text.split()) < 2:
        client.send_message(message.chat.id, "Please provide a YouTube playlist URL.")
        return
    url = message.text.split()[1]
    download_playlist(url, chat_id=message.chat.id)

