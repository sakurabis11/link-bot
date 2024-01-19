
import os
import tempfile

from pyrogram import Client, filters
from shazamio import Shazam

# Initialize the Shazam client
shazam = Shazam()

# Define the command handler for /shazam
@Client.on_message(filters.command("shazam"))
async def shazam_command(client, message):
    # Check if the user has replied to a message with media
    if not message.reply_to_message:
        await message.reply("Please reply to a message with an audio or video file.")
        return

    # Get the media file from the replied message
    media = message.reply_to_message.media

    # Download the media file to a temporary file
    with tempfile.NamedTemporaryFile() as temp_file:
        await client.download_media(media, file_name=temp_file.name)

        # Identify the song using Shazam
        try:
            result = shazam.recognize_song(temp_file.name)
        except Exception as e:
            await message.reply("Sorry, I couldn't identify the song.")
            return

        # Send the song information to the user
        await message.reply(f"Title: {result['track']['title']}\n"
                            f"Artist: {result['track']['artist']}\n"
                            f"Album: {result['track']['album']['title']}")

