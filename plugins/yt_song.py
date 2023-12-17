from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch

DOWNLOAD_DIR = "downloads"

@Client.on_message(filters.command("yt_song"))
async def yt_song_handler(client, message):
    if len(message.text.split()) < 2:
        await message.reply("Please provide a YouTube link or search query!")
        return

    if len(message.text.split()) == 2:
        # Assume URL search
        try:
            youtube_url = YoutubeSearch(message.text.split()[1]).first()["link"]
        except:
            await message.reply("Couldn't find any videos for that query!")
            return
    else:
        youtube_url = message.text.split()[1]

    # Download options
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

    # Download and send song
    await message.reply(f"Downloading song: {yt.title}")
    downloaded_file = stream.download(filename=f"{DOWNLOAD_DIR}/{yt.title}.mp3")
    await client.send_audio(message.chat.id, downloaded_file)

