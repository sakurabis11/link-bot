from pyrogram import Client, filters
from pyrogram.errors import *
from pytube import YouTube
from yt_dlp import YoutubeDL


# Download options
ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}


@Client.on_message(filters.command("yt"))
async def handle_message(client, message):
    url = message.text.split(" ")[1]

    try:
        # Check if it's a playlist link
        if "playlist" in url:
            ydl = YoutubeDL(ydl_opts)
            info = ydl.extract_info(url, download=False)
            song_list = [entry["title"] for entry in info["entries"]]

            # Download and send individual songs
            for song_title, song_info in info["entries"].items():
                song_url = song_info["url"]
                filename = f"{song_title}.mp3"

                try:
                    ydl.download([song_url])
                    with open(filename, "rb") as f:
                        audio = File(f)
                        message.reply_audio(audio)
                finally:
                    os.remove(filename)

            text = f"Downloaded songs from playlist: {', '.join(song_list)}"
            message.reply(text)
            return

        # Download audio from video link
        # Existing code for downloading and sending audio remains unchanged
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")
