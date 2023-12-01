# pattu == music

import asyncio
import os
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch
from soundcloud import Client as SoundcloudClient


@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    song_name = message.text

    if not song_name:
        await client.send_message(message.chat.id, "Please provide a song name to search. Usage: /song (song_name) or (song_name + Artist_name)")
        return

    # Search for the song on YouTube and SoundCloud
    youtube_results = YoutubeSearch(song_name, max_results=1).to_dict()
    soundcloud_results = SoundcloudClient().tracks.search(q=song_name, limit=1)

    # If a search result is found on both YouTube and SoundCloud, present the user with a choice.
    if youtube_results and soundcloud_results:
        await client.send_message(message.chat.id, "Song found on both YouTube and SoundCloud. Choose the source:\n1. YouTube\n2. SoundCloud")

        choice = await message.reply(filters.text())
        if choice.text == "1":
            download_from_youtube(message, youtube_results[0]["url_suffix"], youtube_results[0]["title"])
        elif choice.text == "2":
            download_from_soundcloud(message, soundcloud_results.tracks[0].permalink_url)
        else:
            await client.send_message(message.chat.id, "Invalid choice. Please enter 1 or 2.")
        return

    # If a search result is found on only one platform, proceed with the download.
    if youtube_results:
        download_from_youtube(message, youtube_results[0]["url_suffix"], youtube_results[0]["title"])
    elif soundcloud_results:
        download_from_soundcloud(message, soundcloud_results.tracks[0].permalink_url)
    else:
        await client.send_message(message.chat.id, "Song not found on either YouTube or SoundCloud.")


def download_from_youtube(message, song_url, song_title):
    # Download the song using pytube
    yt = YouTube(f"https://www.youtube.com{song_url}")
    video = yt.streams.filter(only_audio=True).first()
    audio_filename = f"{song_title}.mp3"

    try:
        video.download(filename=audio_filename)
        await message.reply(f"**Song downloaded: {audio_filename}**")

        # Send the downloaded song to the user
        await message.reply_audio(audio_filename)

        # Delete the downloaded song after sending it
        os.remove(audio_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")


def download_from_soundcloud(message, soundcloud_url):
    # Download the song using the SoundCloud API
    soundcloud_client = SoundcloudClient()
    track = soundcloud_client.tracks(soundcloud_url)
    audio_filename = f"{track.title}.mp3"

    try:
        track.stream().download(audio_filename)
        await message.reply(f"**Song downloaded: {audio_filename}**")

        # Send the downloaded song to the user
        await message.reply_audio(audio_filename)

        # Delete the downloaded song after sending it
        os.remove(audio_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")
