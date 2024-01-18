import asyncio
import os
import shutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from yt_dlp import YoutubeDL

@Client.on_message(filters.command("song"))
async def download_song(client, message):
    # Extract the song name from the command
    song_name = message.text.split()[1]

    # Use yt-dlp to download the song
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        song_info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        song_url = song_info["entries"][0]["webpage_url"]
        ydl.download([song_url])

    # Set the thumbnail to the audio file as mp3
    thumb_url = song_info["entries"][0]["thumbnails"][0]["url"]
    thumb_file = "thumbnail.jpg"
    await asyncio.gather(
        client.download_media(thumb_url, thumb_file),
        shutil.move(f"{song_name}.mp3", "song.mp3"),
    )

    # Create an inline keyboard for the user to select the song
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Download Song", callback_data="download_song")]]
    )

    # Send a message with the song details and the inline keyboard
    await message.reply_audio(
        "song.mp3",
        caption=f"{song_info['entries'][0]['title']}\n\n{song_info['entries'][0]['description']}",
        reply_markup=keyboard,
    )

# Define the callback handler for downloading the song
@Client.on_callback_query(filters.regex("download_song"))
async def download_song_callback(client, callback_query):
    # Send the song file to the user
    await client.send_audio(
        callback_query.message.chat.id,
        "song.mp3",
        caption="Your song is ready!",
    )

    # Delete the downloaded files
    os.remove("song.mp3")
    os.remove("thumbnail.jpg")


