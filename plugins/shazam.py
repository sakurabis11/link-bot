import os
import tempfile

import pyrogram
from pyrogram import Client, filters
from shazamio import Shazam

# Replace with your actual API keys
api_id = 1234567  # Replace with your Pyrogram API ID
api_hash = "your_api_hash"  # Replace with your Pyrogram API hash

# Initialize the Shazam client
shazam = Shazam()

# Initialize the Pyrogram client
app = Client("my_shazam_bot", api_id=api_id, api_hash=api_hash)

# Define the command handler for /shazam
@app.on_message(filters.command("shazam"))
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

        try:
            # Identify the song using Shazam
            result = shazam.recognize_song(temp_file.name)

            # Send the song information to the user
            await message.reply(
                f"Title: {result['track']['title']}\n"
                f"Artist: {result['track']['artist']}\n"
                f"Album: {result['track']['album']['title']}"
            )
        except ShazamioError as e:
            await message.reply("Sorry, I couldn't identify the song.")
        except Exception as e:
            # Log the unexpected error for debugging
            print(f"An unexpected error occurred: {e}")
            await message.reply("An error occurred. Please try again later.")


