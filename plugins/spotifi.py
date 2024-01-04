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

@Client.on_message(filters.command("spoti"))
async def music(client, message):
    try:
        track_id = " ".join(message.command[1:])

        # Fetch song information
        results = sp.track(track_id)
        song = results['tracks'][0]

        # Extract song information
        song_info = {
            "artist": song["artists"][0]["name"],
            "title": song["name"],
            "duration": song["duration_ms"],
            "preview_url": song["preview_url"],
            "album_cover": song["album"]["images"][0]["url"]  # Get album cover URL
        }

        # Send thumbnail and details
        await client.send_photo(
            message.chat.id,
            song_info['album_cover'],
            caption=f"**Artist:** {song_info['artist']}\n**Title:** {song_info['title']}\n**Duration:** {song_info['duration'] // 1000} seconds",
            reply_to_message_id=message.id
        )

        # Send chat action to indicate audio uploading
        await client.send_chat_action(message.chat.id, "upload_audio")

        # Fetch full audio (replace with your method for obtaining full audio)
        full_audio_url = await fetch_full_audio(track_id)  # Assuming you have a function for this

        # Send the full audio
        await client.send_audio(
            message.chat.id,
            full_audio_url,
            title=song_info['title'],
            performer=song_info['artist'],
            reply_to_message_id=message.id
        )

    except Exception as e:
        logging.error(f"Error fetching song information or audio: {e}")
        await client.send_message(message.chat.id, "An error occurred. Please try again later.")
