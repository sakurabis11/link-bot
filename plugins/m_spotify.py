
import asyncio
import os
import re
import shutil
import ffmpeg
from pyrogram import Client, filters

@Client.on_message(filters.regex(r"https://open.spotify\.com/.*"))
async def download_command(client, message):
    # Extract the Spotify URL from the message
    spotify_url = message.text

    # Check if the URL is valid
    if not spotify_url.startswith("https://open.spotify.com/"):
        await message.reply_text("Invalid Spotify URL. Please try again.")
        return

    # Download the Spotify audio file
    try:
        await message.reply_text("Downloading...")
        audio_file = await download_spotify_audio(spotify_url)
    except Exception as e:
        await message.reply_text(f"Error downloading audio file: {e}")
        return

    # Send the downloaded audio file to the user
    await message.reply_audio(audio_file, caption=f"Here is the audio file for the Spotify URL you sent: {spotify_url}")

# Define the function to download the Spotify audio file
async def download_spotify_audio(spotify_url):
    # Create a temporary directory to store the downloaded audio file
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # Download the Spotify audio file using ffmpeg
    audio_file_path = os.path.join(temp_dir, "audio.mp3")
    command = f"ffmpeg -i {spotify_url} -f mp3 -vn {audio_file_path}"
    await asyncio.subprocess.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    # Return the path to the downloaded audio file
    return audio_file_path


