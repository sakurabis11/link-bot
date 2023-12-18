import asyncio
import os
import re
from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch
import spotipy
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET 

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))

@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    # Check if user provided song name
    if len(message.text.split()) < 2:
        await message.reply("Please provide the song name you want to download")
        return

    song_name = message.text.split()[1:]  # Extract song name from message
    song_name = " ".join(song_name)  # Combine song name parts

    # Search for song on YouTube
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]

    # Check for Spotify URI
    spotify_uri_regex = r"^spotify:(track|album|playlist):[a-zA-Z0-9]+"
    spotify_uri_match = re.match(spotify_uri_regex, message.text)

    if spotify_uri_match:
        # Extract URI type and ID
        uri_type, uri_id = spotify_uri_match.groups()

        # Build message and send with Spotify URL button
        if uri_type == "track":
            message = f"Open song in Spotify? You can listen to '{song_name}' on Spotify directly."
        elif uri_type == "album":
            message = f"Open album in Spotify? You can listen to '{song_name}' and other songs from the album on Spotify directly."
        else:
            message = f"Open playlist in Spotify? You can listen to '{song_name}' and other songs from the playlist on Spotify directly."

        await message.reply(message, reply_markup=KeyboardButton(text="Open on Spotify", url=f"https://open.spotify.com/{uri_type}/{uri_id}"))
        return

    # Use Spotipy to search for song on Spotify
    spotify_results = sp.search(q=f"{song_name} + {artist}", type="track")

    # Check if results found
    if spotify_results["tracks"]["items"]:
        spotify_track = spotify_results["tracks"]["items"][0]
        spotify_url = spotify_track["uri"]

        # Add Spotify URL message
        message = f"Found '{song_name}' on Spotify: {spotify_url}"
        await message.reply(message)

    # Download song from YouTube
    yt = YouTube(f"https://www.youtube.com{song_url}")
    audio_streams = yt.streams.filter(only_audio=True)

    if not audio_streams:
        await message.reply("No audio stream found for the specified video")
        return

    video = audio_streams.first()
    audio_filename = f"{song_title}.mp3"

    try:
        video.download(filename=audio_filename)
        await message.reply(f"**Song downloaded: {audio_filename}**")

        # Send downloaded song and delete after sending
        await message.reply_audio(audio_filename)
        os.remove(audio_filename)
    except Exception as e:
        await message.reply(f"Error downloading song: {e}")



