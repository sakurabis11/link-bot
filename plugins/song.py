import asyncio
import os
import re
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    # Check if song name provided
    if len(message.text.split()) < 2:
        await message.reply("Please provide the song name you want to download")
        return

    song_name = message.text.split()[1:]
    song_name = " ".join(song_name)

    # Search and download with processing emoji
    await message.reply("⏳ Searching...")
    await asyncio.sleep(1)
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]

    yt = YouTube(f"https://www.youtube.com{song_url}")
    audio_streams = yt.streams.filter(only_audio=True)

    if not audio_streams:
        await message.reply("No audio stream found for the specified video")
        return

    video = audio_streams.first()
    audio_filename = f"{song_title}.mp3"

    try:
        video.download(filename=audio_filename)
        duration = youtube_dl.utils.time_format(video.duration)
        await message.reply_audio(
            audio_filename,
            caption=f"**{song_title} - {duration}**\n[Watch on YouTube](https://www.youtube.com{song_url})",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Send me personally", callback_data=f"send_{audio_filename}")]])
        )

        # Delete downloaded file after sending
        os.remove(audio_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")

@Client.on_callback_query()
async def send_personal_song(client, callback_query):
    callback_data = callback_query.data
    if callback_data.startswith("send_"):
        audio_filename = callback_data[5:]
        await client.send_audio(callback_query.message.sender.id, audio_filename)
        os.remove(audio_filename)
        await callback_query.answer()

