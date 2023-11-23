import pyrogram
from pyrogram import Client, filters
from pytube import YouTube
import os
from info import API_ID, API_HASH, BOT_TOKEN, PORT

@Client.on_message(filters.text)
async def handle_message(message):
    if message.text.startswith("/download "):
        song_name = message.text[8:]

        # Search for the song on YouTube
        try:
            yt = YouTube(f"https://www.youtube.com/results?search_query={song_name}")
        except (pytube.exceptions.PytubeError, pytube.exceptions.ExtractError) as e:
            await message.reply_text(f"An error occurred while searching for the song: {e}")
            return

        # Download the first video result as an MP3 file
        try:
            audio_stream = yt.streams.filter(only_audio=True).first()
            file_name = f"{song_name}.mp3"
            await audio_stream.download(filename=file_name)
        except (pytube.exceptions.ExtractError, pytube.exceptions.PytubeError) as e:
            await message.reply_text(f"An error occurred while downloading the song: {e}")
            return

        # Send the downloaded MP3 file to the user
        await message.reply_document(document=file_name, caption="Here is your song!")

        # Delete the downloaded MP3 file to save storage space
        try:
            os.remove(file_name)
        except (FileNotFoundError, PermissionError) as e:
            await message.reply_text(f"An error occurred while deleting the song file: {e}")
            pass
