import asyncio
import os
import pytube
from pyrogram import Client, filters

@Client.on_message(filters.command(["download"]))
async def download_song(client, message):
    if message.chat.id != message.from_user.id:
        return

    if message.reply_to_message is None or message.reply_to_message.text is None:
        await message.reply_text("Please reply to a message containing a Spotify song link.")
        return

    spotify_link = message.reply_to_message.text

    try:
        # Extract song details from Spotify link
        yt = pytube.YouTube(spotify_link)
        song_title = yt.title
        song_artist = yt.author

        # Download the song
        video = yt.streams.first()
        video.download(filename=f"{song_title}.mp4")

        # Convert MP4 to MP3
        os.system(f"ffmpeg -i {song_title}.mp4 -q:a 0 -b:a 192k {song_title}.mp3")

        # Send the downloaded MP3 file to the user
        await message.reply_document(f"{song_title}.mp3")

        # Delete the temporary files
        os.remove(f"{song_title}.mp4")
        os.remove(f"{song_title}.mp3")

        await message.reply_text(f"✅ Song downloaded: {song_title} by {song_artist}")
    except Exception as e:
        await message.reply_text(f"❌ Error downloading song: {e}")
