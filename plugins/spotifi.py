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

# Define the command handler for /song
@Client.on_message(filters.command("ring"))
async def music(client, message):
    # Extract the query from the command message
    query = " ".join(message.command[1:])

    # Check if a query is provided
    if not query:
        await client.send_message(message.chat.id, "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ sᴏɴɢ ɴᴀᴍᴇ ᴛᴏ sᴇᴀʀᴄʜ. ᴜsᴀɢᴇ: /ringtune (song_name) or (song_name + Artist_name)")
        return
    await client.send_message(REQUESTED_CHANNEL, text=f"#ʀɪɴɢᴛᴜɴᴇ\nʀᴇǫᴜᴇsᴛᴇᴅ ғʀᴏᴍ {message.from_user.mention}\nʀᴇǫᴜᴇsᴛ ɪs {query}")

    try:
        # Search for the song on Spotify
        results = sp.search(q=query, type="track")
        tracks = results['tracks']['items']

        if not tracks:
            await client.send_message(message.chat.id, "ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ ғᴏʀ ᴛʜᴇ ɢɪᴠᴇɴ {query}.")
            return

        # Get the first result
        song = tracks[0]

        # Extract song information
        song_info = {
            "artist": song["artists"][0]["name"],
            "title": song["name"],
            "duration": song["duration_ms"],  # Spotify uses milliseconds
            "preview_url": song["preview_url"],
        }

        # Send a message to the user with the song details and a download link
        await client.send_message(message.chat.id, f"ʜᴇʏ {message.from_user.mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ {query}\n\n ᴀʀᴛɪsᴛ: {song_info['artist']}\n ᴛɪᴛʟᴇ: {song_info['title']}\n⌛ ᴅᴜʀᴀᴛɪᴏɴ: {song_info['duration'] // 1000} sᴇᴄᴏɴᴅs\n\nʏᴏᴜ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜɪs sᴏɴɢ ғʀᴏᴍ ᴄʜʀᴏᴍᴇ: {song_info['preview_url']}")

        # Send chat action to indicate that the bot is uploading audio
        await client.send_chat_action(message.chat.id, "upload_audio")

        # Send the audio preview
        await client.send_audio(message.chat.id, song_info['preview_url'], title=song_info['title'], performer=song_info['artist'], reply_to_message_id=message.id)

    except Exception as e:
        logging.error(f"Error fetching song information: {e}")
        await client.send_message(message.chat.id, "An error occurred while fetching the song information. Please try again later.")
