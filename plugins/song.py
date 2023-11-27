import wget
import discord
import requests
from asyncio import sleep
from info import LOG_CHANNEL

@client.on_message(filters.command('ssong') & filters.text)
async def song(client, message):
    args = message.text.split(None, 1)[1]
    if not args:
        return await message.reply("/ssong requires an argument.")

    # Download the song

    pak = await message.reply('Downloading...')
    try:
        response = requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1").json()
    except Exception as e:
        await pak.edit(str(e))
        return

    # Extract song information

    sname = response['data']['results'][0]['name']
    slink = response['data']['results'][0]['downloadUrl'][4]['link']
    ssingers = response['data']['results'][0]['primaryArtists']
    thumbnail_url = response['data']['results'][0]['image'][2]['link']

    # Download the thumbnail

    thumbnail = await download_image(thumbnail_url)

    # Download the song file

    file = await download_song(slink)

    # Convert MP4 to MP3

    mp3_file = convert_mp4_to_mp3(file)

    # Send the song message

    await pak.edit('Uploading...')
    await message.reply_audio(audio=mp3_file, title=sname, performer=ssingers, caption=f"[{sname}]({response['data']['results'][0]['url']}) - from saavn ",thumb=thumbnail)

    # Cleanup

    os.remove(mp3_file)
    os.remove(thumbnail)
    await pak.delete()

    # Log the request

    await client.send_message(LOG_CHANNEL, f"<@{message.from_user.id}> requested a song: {sname}")


async def download_image(url):
    filename = f"song_thumbnail.{url.split('.')[-1]}"
    await wget.download(url, filename)
    return filename


async def download_song(url):
    filename = f"song.{url.split('.')[-1]}"
    await wget.download(url, filename)
    return filename


def convert_mp4_to_mp3(filename):
    mp3_filename = filename.replace("mp4", "mp3")
    os.system(f"ffmpeg -i {filename} {mp3_filename}")
    return mp3_filename
