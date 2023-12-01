import asyncio
import pyrogram
from pyrogram import filters, Client
from scdl import *
import re


@Client.on_message(filters.command("soundcloud"))
async def handle_message(client, message):
    # Check if the message starts with the command "soundcloud"
    if message.text.startswith('soundcloud'):
        # Extract the SoundCloud track URL from the message
        track_url = message.text.split(' ')[1]

        # Download the song using scdl
        try:
            song = await scdl.download(track_url)
        except scdl.Error as e:
            await message.reply(f'Error downloading song: {e.message}')
            return

        # Send the downloaded song to the user
        await message.reply_document(song, filename=song.split('/')[-1])
