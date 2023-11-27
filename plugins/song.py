import async_requests
import discord
import os
import re
import wget
from asyncio import sleep
from aioffmpeg import input, output
from loguru import logger

LOG_CHANNEL = "YOUR_LOG_CHANNEL_ID"


@client.on_message(filters.command("song") & filters.text)
async def song(client, message):
    try:
        args = message.text.split(None, 1)[1]
        # Check if an argument is provided
        if not args:
            raise ValueError("/song {song_name}.")

        # Download the song
        logger.info(f"Downloading song: {args}")
        pak = await message.reply('Downloading...')
        response = await async_requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1")
        response_json = await response.json()
        song_info = response_json['data']['results'][0]

        # Extract song information
        song_name = song_info['name']
        song_url = song_info['downloadUrl'][4]['link']
        song_artists = song_info['primaryArtists']

        # Download the thumbnail image
        thumbnail_url = song_info['image'][2]['link']
        thumbnail_filename = f"song_thumbnail.{thumbnail_url.split('.')[-1]}"
        await wget.download(thumbnail_url, thumbnail_filename)

        # Download the song file and convert it to MP3
        song_filename = f"song.{song_url.split('.')[-1]}"
        await wget.download(song_url, song_filename)
        mp3_filename = song_filename.replace("mp4", "mp3")
        await convert_to_mp3(song_filename, mp3_filename)

        # Send the song message
        await pak.edit('Uploading...')
        await message.reply_audio(audio=mp3_filename, title=song_name, performer=song_artists, caption=f"[{song_name}]({song_info['url']}) - from saavn ",thumb=thumbnail_filename)

        # Cleanup
        os.remove(mp3_filename)
        os.remove(thumbnail_filename)
        await pak.delete()

        # Log the request
        logger.info(f"Song request: {message.from_user.id} - {song_name}")

    except Exception as e:
        logger.error(e)
        await message.reply(f"Error: {e}")


async def convert_to_mp3(input_filename, output_filename):
    async with input(input_filename), output(output_filename):
        await output.overwrite_output(True)
        await output.global_args('-codec:a libmp3lame')
        await output.run()
