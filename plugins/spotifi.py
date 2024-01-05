import os
import logging
from pyrogram import Client, filters, enums
import requests
import json
from info import REQUESTED_CHANNEL, SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define the command handler for /song
@Client.on_message(filters.command("tune"))
async def music(client, message):
    query = " ".join(message.command[1:])

    if not query:
        await client.send_message(message.chat.id, "Please provide a song name to search. Usage: /ringtune (song_name) or (song_name + Artist_name)")
        return

    await client.send_message(REQUESTED_CHANNEL, text=f"#ʀɪɴɢᴛᴜɴᴇ\nRequested from {message.from_user.mention}\nRequest is {query}")

    try:
        results = sp.search(q=query, type="track")
        tracks = results['tracks']['items']

        if not tracks:
            await client.send_message(message.chat.id, f"No results found for the given {query}.")
            return

        song = tracks[0]
        song_info = {
            "artist": song["artists"][0]["name"],
            "title": song["name"],
            "duration": song["duration_ms"],  # Spotify uses milliseconds
            "preview_url": song["preview_url"],
        }

        # Send the audio preview first
        await client.send_chat_action(message.chat.id, "upload_audio")
        await client.send_audio(
            message.chat.id,
            song_info['preview_url'],
            title=song_info['title'],
            performer=song_info['artist'],
            reply_to_message_id=message.id
        )

        # Now send the message with song details and download link
        await client.send_message(
            message.chat.id,
            f"Hey {message.from_user.mention},\n\nYour request {query}\n\nArtist: {song_info['artist']}\nTitle: {song_info['title']}\n⌛ Duration: {song_info['duration'] // 1000} seconds\n\nYou can download this song from Chrome: {song_info['preview_url']}"
        )

    except Exception as e:
        logging.error(f"Error fetching song information: {e}")
        await client.send_message(message.chat.id, "An error occurred while fetching the song information. Please try again later.")
