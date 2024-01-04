import os
import logging
from pyrogram import Client, filters, enums
import requests
import json
from info import REQUESTED_CHANNEL, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define the regular expression pattern for matching Spotify track URLs
spotify_url_regex = r"https://open\.spotify\.com/track/(.+?)"

# Define the command handler using a regular expression filter
@Client.on_message(filters.regex(spotify_url_regex))
async def music(client, message):
    # Extract the track ID from the URL
    track_id = message.text

    # Fetch song information using the track ID
    try:
        results = sp.track(track_id)
        song = results['tracks'][0]

        # Extract song information
        song_info = {
            "artist": song["artists"][0]["name"],
            "title": song["name"],
            "duration": song["duration_ms"],  # Spotify uses milliseconds
            "preview_url": song["preview_url"],
        }

        # Send a message to the user with the song details and a download link
        await client.send_message(message.chat.id, f"Hey {message.from_user.mention},\n\nYour request:\n\nArtist: {song_info['artist']}\nTitle: {song_info['title']}\n⏳ Duration: {song_info['duration'] // 1000} seconds\n\nYou can download this song from Chrome: {song_info['preview_url']}")

        # Send chat action to indicate that the bot is uploading audio
        await client.send_chat_action(message.chat.id, "upload_audio")

        # Send the audio preview
        await client.send_audio(message.chat.id, song_info['preview_url'], title=song_info['title'], performer=song_info['artist'], reply_to_message_id=message.id)

    except Exception as e:
        logging.error(f"Error fetching song information: {e}")
        await client.send_message(message.chat.id, "An error occurred while fetching the song information. Please try again later.")
