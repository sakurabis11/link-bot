import asyncio
import pyrogram
from scdl import *

# Initialize Pyrogram
app = pyrogram.Client('my_bot', api_id=12345, api_hash='my_api_hash')

# Define the bot's event handler
@app.on_message(filters.command("soundcloud"))
async def handle_message(client, message):
    # Check if the message starts with the command "soundcloud"
    if message.text.startswith('soundcloud'):
        # Extract the SoundCloud track URL from the message
        track_url = message.text.split(' ')[1]

        # Download the song using scdl
        try:
            song = await scdl.download(track_url)
        except Exception as e:
            await message.reply(f'Error downloading song: {e}')
            return

        # Send the downloaded song to the user
        await message.reply_document(song, filename=song.split('/')[-1])
