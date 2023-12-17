from pyrogram import Client, filters
from youtube_dl import YoutubeDL
import ffmpeg

@Client.on_message(filters.command("yt_song"))
async def yt_download(client, message):
    if len(message.text.split()) < 2:
        await message.reply_text("Please provide a YouTube link.")
        return

    youtube_url = message.text.split()[1]

    # Use youtube-dl to extract data
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        song_title = info_dict["title"]

    # Download and send audio file
    try:
        ydl.download([youtube_url])
        file_path = f"{song_title}.mp3"
        await message.reply_audio(file_path)
    except Exception as e:
        await message.reply_text(f"Error downloading song: {e}")
    finally:
        # Remove downloaded file
        os.remove(file_path)

