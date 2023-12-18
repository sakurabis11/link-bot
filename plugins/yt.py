from pyrogram import Client, filters
from pyrogram.errors import RPC_METHOD_NOT_AVAILABLE
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

                text = " Found Playlist:\n" + "\n".join(song_list)
                message.reply(text)
                return

            # Download audio from video link
            ydl = YoutubeDL(ydl_opts)
            info = ydl.extract_info(url, download=False)
            filename = f"{info['title']}.mp3"

            try:
                # Download and send audio
                ydl.download([url])
                with open(filename, "rb") as f:
                    audio = File(f)
                    message.reply_audio(audio)
            finally:
                # Remove downloaded file
                os.remove(filename)

        except (IndexError, RPC_METHOD_NOT_AVAILABLE, Exception) as e:
            message.reply(f"❌ Error: {e}")

