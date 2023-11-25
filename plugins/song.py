import asyncio
import pyrogram
import requests, os, wget
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command('song') & filters.text)
async def download_song(song_name, chat_id):
    try:
        song_name = message.text.split(None, 1)[1]
    except:
        await message.reply("Please send the song name.")
        return ""

    if not song_name:
        await message.reply("Please send the song name.")
        return ""

    await message.reply("Searching for the song...")

    # Download the song in a separate task to prevent blocking the main thread
    asyncio.create_task(download_song(song_name, message.chat.id))

        # Get song information
        response = requests.get(f"https://saavn.me/search/songs?query={song_name}&page=1&limit=1").json()
        song_data = response['data']['results'][0]

        # Extract song details
        song_title = song_data['name']
        song_artists = song_data['primaryArtists']
        song_download_url = song_data['downloadUrl'][4]['link']

        # Download thumbnail image
        thumbnail_url = song_data['image'][2]['link']
        thumbnail_file = wget.download(thumbnail_url)

        # Download audio file asynchronously
        async with aiofiles.open(f"song_{song_title}.mp3", mode='wb') as f:
            async for chunk in requests.get(song_download_url, stream=True).iter_content(chunk_size=1024):
                await f.write(chunk)

        audio_file = f"song_{song_title}.mp3"

        # Send audio file with metadata and inline buttons
        await bot.send_audio(chat_id, audio=audio_file, title=song_title, performer=song_artists,
                             thumb=thumbnail_file)

        # Remove temporary files
        os.remove(audio_file)
        os.remove(thumbnail_file)

    except Exception as e:
        await bot.send_message(chat_id, f"An error occurred while downloading the song: {e}")
