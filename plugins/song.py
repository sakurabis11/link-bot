import pyrogram
from pyrogram import Client, filters
from pytube import YouTube
import os

bot = Client("my_bot", api_id=123456789, api_hash="abcdefghijklmnopqrstuvwxyz")

@Client.on_message(filters.text)
async def handle_message(message):
    if message.text.startswith("/download "):
        song_name = message.text[8:]

        # Search for the song on YouTube
        yt = YouTube(f"https://www.youtube.com/results?search_query={song_name}")

        # Download the first video result as an MP3 file
        audio_stream = yt.streams.filter(only_audio=True).first()
        file_name = f"{song_name}.mp3"
        await audio_stream.download(filename=file_name)

        # Send the downloaded MP3 file to the user
        await message.reply_document(document=file_name, caption="Here is your song!")

        # Delete the downloaded MP3 file to save storage space
        os.remove(file_name)

