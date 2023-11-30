import asyncio
import os
import requests
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch
from PIL import Image


@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    song_name = message.text

    # Search for the song on YouTube
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]
    song_artist = search_results[0]["artist"]
    song_album = search_results[0]["album"]
    song_duration = search_results[0]["duration"]

    # Download the thumbnail image
    thumbnail_url = f"https://img.youtube.com/vi/{song_url}/hqdefault.jpg"
    thumbnail_response = requests.get(thumbnail_url, stream=True)

    if thumbnail_response.status_code == 200:
        with open("thumbnail.jpg", "wb") as thumbnail_file:
            for chunk in thumbnail_response.iter_content(1024):
                thumbnail_file.write(chunk)

        thumbnail_image = Image.open("thumbnail.jpg")
        thumbnail_image.resize((200, 200))
        thumbnail_image.save("thumbnail_resized.jpg")

        # Send the thumbnail image along with song information
        await message.reply_photo(
            "thumbnail_resized.jpg",
            caption=f"**Title:** {song_title}\n**Artist:** {song_artist}\n**Album:** {song_album}\n**Duration:** {song_duration}",
        )

        # Download and send the song file
        yt = YouTube(f"https://www.youtube.com{song_url}")
        video = yt.streams.filter(only_audio=True).first()
        audio_filename = f"{song_title}.mp3"

        try:
            video.download(filename=audio_filename)
            await message.reply(f"**Song downloaded: {audio_filename}**")
            await message.reply_audio(audio_filename)
            os.remove(audio_filename)
        except Exception as e:
            await message.reply(f"Error downloading song: {e}")

        os.remove("thumbnail_resized.jpg")
    else:
        await message.reply(f"Error downloading thumbnail: {thumbnail_response.status_code}")
