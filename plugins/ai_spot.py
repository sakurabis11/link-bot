python
import asyncio
import re

from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.file_id import FileId
from pyrogram.types import Message

# Spotify URL Regex
SPOTIFY_URL_REGEX = r"https://open\.spotify\.com/(track|album)/(?P[a-zA-Z0-9]+)"

# Regex filter to match Spotify URLs
spotify_url_filter = filters.create(lambda _, __, message: bool(re.match(SPOTIFY_URL_REGEX, message.text)))

# Message handler for Spotify URLs
@Client.on_message(spotify_url_filter)
async def download_spotify_song(client: Client, message: Message):
    # Extract the Spotify song URL
    spotify_url = message.text
    match = re.match(SPOTIFY_URL_REGEX, spotify_url)
    song_id = match.group("id")

    await message.reply_text = f"{song_id}"

    # Get the song metadata
    metadata = await client.get_media(f"https://open.spotify.com/track/{song_id}")

    # Download the song
    try:
        file_id = await client.download_media(metadata.audio.file_id)
    except RPCError as e:
        message.reply("Sorry, I couldn't download the song. Please try again.")
        return

    # Send the downloaded song
    await client.send_audio(
        chat_id=message.chat.id,
        audio=FileId(file_id),
        caption=f"**{metadata.title}** by **{metadata.artist}**",
        reply_to_message_id=message.id,
    )


