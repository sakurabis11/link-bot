import os
import requests
from os import environ
from pyrogram import Client, filters
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "d3a0f15a75014999945b5628dca40d0a",
SPOTIFY_CLIENT_SECRET = "e39d1705e35c47e6a0baf50ff3bb587f"

# Create a Spotify client instance
spotify = Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                             client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                             redirect_uri='http://localhost:8080'))

# Define a command handler for the `/spotify` command
@Clientt.on_message(filters.command('spotify'))
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

