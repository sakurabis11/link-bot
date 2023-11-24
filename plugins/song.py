from pyrogram import Client, filters
import requests
import os
import asyncio


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

        # Extract song URL, name, artist, album, and genre
        song_url = song_data[song_id]['media_preview_url'].replace("preview", "aac")
        song_name = song_data[song_id]['song']
        artist = song_data[song_id]['artist']
        album = song_data[song_id]['album']
        genre = song_data[song_id]['genre']

        # Download song file
        r = await asyncio.to_thread(requests.get, song_url)
        with open(f"{song_name}.mp3", 'wb') as f:
            f.write(r.content)

        # Send audio file to chat with song information
        audio = open(f"{song_name}.mp3", 'rb')
        await client.send_audio(chat_id=message.chat.id, audio=audio, caption=f"{song_name} by {artist} from the album {album} ({genre})")

        # Remove temporary file
        await asyncio.to_thread(os.remove, f"{song_name}.mp3")
    except Exception as e:
        await client.send_message(chat_id=message.chat.id, text=f"An error occurred while downloading the song: {e}")
