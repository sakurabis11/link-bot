import os
import requests
from pyrogram import Client, filters
from pyrogram.types import *
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotdl

# Define your client id and client secret
client_id = 'd3a0f15a75014999945b5628dca40d0a'
client_secret = 'e39d1705e35c47e6a0baf50ff3bb587f'

# Set up spotipy with your client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@Client.on_message(filters.command("spoti"))
async def spotify(client, message):
    # Get the song name or Spotify URL from the command
    song_name_or_url = message.command[1:]
    song_name_or_url = " ".join(song_name_or_url)

    # Check if the command argument is a Spotify URL
    match = re.match(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)', song_name_or_url)
    if match:
        # If it is a Spotify URL, extract the song ID from the URL
        song_id = match.group(1)
    else:
        # If it is not a Spotify URL, search for the song on Spotify
        song_name = song_name_or_url
        results = sp.search(q=song_name, limit=1)
        song_id = results['tracks']['items'][0]['id']

    # Get the song details from Spotify
    track = sp.track(song_id)
    artist = track['artists'][0]['name']
    name = track['name']
    album = track['album']['name']
    release_date = track['album']['release_date']
    popularity = track['popularity']

    # Download the song from Spotify
    song_url = f"https://open.spotify.com/track/{song_id}"
    spotdl.download_track(song_url)

    # Send the song details to the user
    await message.reply_text(f"Title: {name}\nArtist: {artist}\nAlbum: {album}\nRelease Date: {release_date}\nPopularity: {popularity}")

    # Upload the song to Telegram as an mp3 file
    await message.reply_audio(audio=open('song.mp3', 'rb'))
