import asyncio
from pyrogram import Client, filters, enums
import requests
import os
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_message(filters.command("song"))
async def download_song(client, message):
    try:
        query = ' '.join(message.command[1:])

        # Download song information
        response = await asyncio.to_thread(requests.get, f"https://www.jiosaavn.com/api.php?query={query}&__call=autocomplete.get&_format=json&_marker=0")
        data = response.json()

        # Extract song ID
        song_id = data['songs']['data'][0]['id']

        # Download song details
        song_response = await asyncio.to_thread(requests.get, f"https://www.jiosaavn.com/api.php?__call=song.getDetails&pids={song_id}&_format=json&_marker=0&model=SM-G930F")
        song_data = song_response.json()

        # Extract song URL, name
        song_url = song_data[song_id]['media_preview_url'].replace("preview", "aac")
        song_name = song_data[song_id]['song']

        # Download song file
        r = await asyncio.to_thread(requests.get, song_url)
        temp_file = f"{song_name}.mp3"
        with open(temp_file, 'wb') as f:
            f.write(r.content)

        # Send audio file to chat without song information
        audio = open(temp_file, 'rb')
        await client.send_audio(chat_id=message.chat.id, audio=audio)

        # Remove temporary file
        try:
            await asyncio.to_thread(os.remove, temp_file)
        except Exception as e:
            await client.send_message(chat_id=message.chat.id, text=f"Failed to remove temporary file: {e}")

    except Exception as e:
        await client.send_message(chat_id=message.chat.id, text=f"An error occurred while downloading the song: {e}")
