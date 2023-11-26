import asyncio
import requests, os, wget
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command('song'))
async def song(client, message):
    try:
        args = message.text.split(None, 1)[1]
    except:
        return await message.reply("Send the song name.")

    if not args:
        await message.reply("Send the song name..")
        return ""

    # Send a sticker to indicate that the request is being processed
    pak = await client.send_sticker(message.chat.id, 'CAACAgUAAxkBAAJyMWVhaXgwvctsfT0fApCGniRz20upAAKfAwACgSNIVG3KGaDGncrFHgQ')

    try:
        # Search for the song using Saavn API
        response = requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1").json()
    except Exception as e:
        await pak.edit(str(e))
        return

    # Extract song information from the API response
    sname = response['data']['results'][0]['name']
    slink = response['data']['results'][0]['downloadUrl'][4]['link']
    ssingers = response['data']['results'][0]['primaryArtists']

    # Check if the song is available for download
    if not slink:
        await pak.edit("Song not available for download.")
        return

    # Download the thumbnail image
    img = response['data']['results'][0]['image'][2]['link']
    thumbnail = await download_image(img)

    # Download the audio file using asynchronous tasks
    audio_file = await download_audio_async(slink)

    # Generate inline buttons for music streaming services
    spotify_button = InlineKeyboardButton("Spotify", url=f"https://open.spotify.com/search?q={sname}")
    youtube_button = InlineKeyboardButton("YouTube", url=f"https://www.youtube.com/results?search_query={sname}")
    saavn_button = InlineKeyboardButton("Saavn", url=response['data']['results'][0]['url'])

    # Create an inline keyboard markup and add the buttons
    keyboard = InlineKeyboardMarkup([[spotify_button], [youtube_button], [saavn_button]])

    # Send the audio file with metadata and inline buttons
    await message.reply_audio(audio=audio_file, title=sname, performer=ssingers,
                                thumb=thumbnail, reply_markup=keyboard)

    # Remove temporary files
    await delete_files([audio_file, thumbnail])

    # Delete the sticker message
    await pak.delete()

async def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open('thumbnail.jpg', 'wb') as f:
                f.write(response.content)
            return 'thumbnail.jpg'
        else:
            return None
    except Exception as e:
        print(e)
        return None

async def download_audio_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, stream=True) as response:
            total_size = int(response.headers.get('content-length', 0))
            with open('audio.mp4', 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
                    print('\rDownloading: {:.2f}%'.format(os.path.getsize('audio.mp4') / total_size * 100), end='')
            os.rename('audio.mp4', 'audio.mp3')
            print('\nDownload complete.')
            return 'audio.mp3'

async def delete_files(files):
    for file in files:
        try:
            os.remove(file)
        except:
            pass
