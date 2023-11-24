
import asyncio
from pyrogram import Client, filters, enums
import requests
import os

@Client.on_message(filters.command("song"))
async def download_song(client, message):
    try:
        query = ' '.join(message.command[1:])

        response = await asyncio.to_thread(requests.get, f"https://www.jiosaavn.com/api.php?query={query}&__call=autocomplete.get&_format=json&_marker=0")
        data = response.json()

        song_id = data['songs']['data'][0]['id']

        song_response = await asyncio.to_thread(requests.get, f"https://www.jiosaavn.com/api.php?__call=song.getDetails&pids={song_id}&_format=json&_marker=0&model=SM-G930F")
        song_data = song_response.json()

        song_url = song_data[song_id]['media_preview_url'].replace("preview", "aac")
        song_name = song_data[song_id]['song']

        r = await asyncio.to_thread(requests.get, song_url)
        with open(f"{song_name}.mp3", 'wb') as f:
            f.write(r.content)

        inline_query = InlineKeyboardMarkup(1)
        lyrics_button = InlineKeyboardButton(text="Lyrics", callback_data=f"lyrics|{song_name}")
        inline_query.add(lyrics_button)

        await client.send_audio(chat_id=message.chat.id, audio=audio, caption=f"{song_name}", reply_markup=inline_query)

@Client.on_callback_query(filters.regex(r"lyrics\|(.*)"))
async def handle_lyrics_callback(client, callback_query):
            song_name = callback_query.data.split("|")[1]

            response = await asyncio.to_thread(requests.get, f"https://www.musixmatch.com/lyrics/{song_name}")
            lyrics_data = response.json()

            lyrics = lyrics_data['message']['body']['lyrics']['lyrics']

            await client.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=lyrics)

        if os.path.exists(f"{song_name}.mp3"):
            await asyncio.to_thread(os.remove, f"{song_name}.mp3")

    except Exception as e:
        await client.send_message(chat_id=message.chat.id, text=f"An error occurred while downloading the song: {e}")
