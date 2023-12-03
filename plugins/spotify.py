import os
import requests
from os import environ
from pyrogram import Client, filters
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Create a Spotify client instance
spotify = Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                             client_secret=SPOTIFY_CLIENT_SECRET,
                                             redirect_uri=None))

# Define a command handler for the `/spotify` command
@Client.on_message(filters.command('spotify'))
async def download_song(client, message):
    # Extract the song name from the command argument
    song_name = message.text.split(' ')[1]

    # Search for the song on Spotify
    results = spotify.search(q=song_name, type='track')
    if len(results['tracks']['items']) == 0:
        await message.reply_text('Song not found')
        return

    # Get the first song result
    track = results['tracks']['items'][0]

    # Get the song thumbnail
    thumbnail_url = track['album']['images'][0]['url']

    # Get the song details
    song_details = f"**Song:** {track['name']}\n**Artist:** {track['artists'][0]['name']}\n**Album:** {track['album']['name']}"

    # Download the song
    song_url = track['uri']
    response = requests.get(song_url)
    with open('song.mp3', 'wb') as f:
        f.write(response.content)

    # Send the thumbnail, song details, and song file to Telegram
    await message.reply_photo(thumbnail_url)
    await message.reply_text(song_details)
    await message.reply_document('song.mp3')

