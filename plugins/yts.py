import pyrogram
from pyrogram import Client, filters
import yt_dlp

@Client.on_message(filters.command("sng"))
async def download_song(client, message):
    try:
        url = message.text.split(" ", 1)[1]  # Extract the YouTube URL from the message

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            await message.reply_text(f"Downloading {video_title}...")

            ydl.download([url])

            song_path = ydl.prepare_filename(info_dict)
            await client.send_audio(message.chat.id, audio=song_path)

            await message.reply_text(f"Song sent successfully!")

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

