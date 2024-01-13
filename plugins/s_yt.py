python
import asyncio
import os
import re
import shutil
import tempfile

from pyrogram import Client, filters
from pyrogram.types import Message

# Define the regex pattern to match YouTube URLs
YOUTUBE_URL_REGEX = re.compile(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.сом|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")

# Define the function to download a song from a YouTube URL
async def download_song(url):
    # Create a temporary directory to store the downloaded song
    temp_dir = tempfile.mkdtemp()

    # Download the song using youtube-dl
    await asyncio.subprocess.run(
        ["youtube-dl", "-x", "--audio-format", "mp3", "-o", os.path.join(temp_dir, "%(title)s.%(ext)s"), url]
    )

    # Get the downloaded song file path
    song_file = os.path.join(temp_dir, "%(title)s.%(ext)s")

    # Return the song file path and the temporary directory
    return song_file, temp_dir


# Define the function to send a song with a thumbnail
async def send_song(chat_id, song_file, thumbnail_url):
    # Download the thumbnail image
    thumbnail_file = await client.download_media(thumbnail_url)

    # Send the song with the thumbnail
    await client.send_audio(
        chat_id,
        audio=song_file,
        thumb=thumbnail_file,
        caption="Here's your song!",
    )

    # Delete the temporary directory and the downloaded files
    shutil.rmtree(song_file.rsplit("/", 1)[0])
    os.remove(thumbnail_file)


# Define the event handler for downloading and sending songs
@Client.on_message(filters.regex(YOUTUBE_URL_REGEX))
async def download_and_send_song(client: Client, message: Message):
    # Extract the YouTube URL from the message text
    youtube_url = message.text

    # Download the song and get the temporary directory
    song_file, temp_dir = await download_song(youtube_url)

    # Get the thumbnail URL from the YouTube URL
    thumbnail_url = f"https://img.youtube.com/vi/{youtube_url.rsplit('/', 1)[1]}/hqdefault.jpg"

    # Send the song with the thumbnail
    await send_song(message.chat.id, song_file, thumbnail_url)

    # Delete the temporary directory and the downloaded files
    shutil.rmtree(temp_dir)
    os.remove(song_file)



