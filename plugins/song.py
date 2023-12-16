import asyncio
import os
import re
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch


@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    # Check for song name, video link, or playlist link
    if len(message.text.split()) < 2:
        await message.reply("Please provide a song name, YouTube video link, or playlist link.")
        return

    # Extract the input
    input_text = message.text.split()[1]

    # Check if it's a song name
    if re.search(r"\s+", input_text):
        # Search for the song on YouTube
        search_results = YoutubeSearch(input_text, max_results=1).to_dict()
        song_url = search_results[0]["url_suffix"]
        song_title = search_results[0]["title"]
        download_from_url(client, message, f"https://www.youtube.com{song_url}", song_title)
    elif input_text.startswith("https://www.youtube.com/"):
        # Assume it's a YouTube video link
        download_from_url(client, message, input_text, None)
    elif input_text.startswith("https://music.youtube.com/"):
        # Assume it's a YouTube playlist link
        download_playlist(client, message, input_text)
    else:
        await message.reply("Invalid input. Please provide a valid song name, video link, or playlist link.")


def download_from_url(client, message, url, title=None):
    # Download and send the song
    try:
        yt = YouTube(url)
        audio_streams = yt.streams.filter(only_audio=True)
        if not audio_streams:
            raise Exception("No audio stream found for the specified video.")
        video = audio_streams.first()
        filename = f"{title or yt.title}.mp3"
        video.download(filename=filename)
        await message.reply(f"**Song downloaded: {filename}**")
        await message.reply_audio(filename)
        os.remove(filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")


def download_playlist(client, message, playlist_url):
    # Download all songs in the playlist
    try:
        playlist = YouTube(playlist_url).playlist
        for item in playlist.videos:
            download_from_url(client, message, item.url, item.title)
        await message.reply("Playlist downloaded successfully!")
    except Exception as e:
        await message.reply(f"Error downloading playlist: {e}")

