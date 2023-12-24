import pyrogram
from pyrogram import Client, filters
import yt_dlp

@Client.on_message(filters.command("yts"))
async def yts(client, message):
 url = message.text.split(" ", 1)[1]  # Extract URL from message

 try:
   ydl_opts = {
     "format": "bestaudio/best",
     "postprocessors": [
       {
         "key": "FFmpegExtractAudio",
         "preferredcodec": "mp3",
         "preferredquality": "192",
       }
     ],
     "outtmpl": "%(title)s.%(ext)s",
     "noplaylist": True,
   }

   with yt_dlp.YoutubeDL(ydl_opts) as ydl:
     info_dict = ydl.extract_info(url, download=False)
     title = info_dict.get("title", "Unknown Title")
     audio_file = ydl.prepare_filename(info_dict)

     # Download the audio file directly using `ydl.extract_info`
     ydl.extract_info(url, download=True)  # Download the audio file

     await message.reply_audio(audio_file, caption=f"Downloaded song: {title}")
 except Exception as e:
   await message.reply_text(f"An error occurred: {e}")
