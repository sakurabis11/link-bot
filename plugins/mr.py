import os
import logging
from pyrogram import Client, filters, enums
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Create Spotify auth object
auth = SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth)

# Define the command handler for /song
@Client.on_message(filters.command("ringtone"))
async def music(client, message):
    # Extract the query from the command message
    query = " ".join(message.command[1:])

    # Check if a query is provided
    if not query:
        await client.send_message(message.chat.id, "Please provide a song name to search. Usage: /ringtone (song_name) or (song_name + Artist_name)")
        return

    # Search for the song using Spotify API
    try:
        results = sp.search(q=query, type="track")
    except Exception as e:
        logging.error(f"Error searching for song: {e}")
        await client.send_message(message.chat.id, "An error occurred while searching for the song. Please try again later.")
        return

    # Check if any results were found
    if not results["tracks"]["items"]:
        await client.send_message(message.chat.id, f"No results found for the given query: {query}.")
        return

    # Get the first result (most relevant result)
    song = results["tracks"]["items"][0]

    # Create a dictionary to store the song information
    song_info = {
        "artist": song["artists"][0]["name"],
        "title": song["name"],
        "duration": song["duration_ms"] // 1000,
        "preview_url": song["preview_url"],
    }

    # Send a message to the user with the song details and a preview link
    await client.send_message(message.chat.id, f"Hey {message.from_user.mention},\n\nYour request: {query}\n\n Artist: {song_info['artist']}\n Title: {song_info['title']}\n⌛ Duration: {song_info['duration']} seconds\n\nYou can listen to a preview of this song: {song_info['preview_url']}")

    # Send chat action to indicate that the bot is uploading audio
    await client.send_chat_action(message.chat.id, "upload_audio")

    # Check if the message is a reply to another audio message
    if message.reply_to_message and message.reply_to_message.media:
        # If it is, send the audio preview as a reply to the original audio message
        await client.send_audio(message.chat.id, song_info["preview_url"], title=song_info["title"], performer=song_info["artist"], reply_to_message_id=message.reply_to_message.id)
    else:
        # Otherwise, send it as a reply to the original message
        await client.send_audio(message.chat.id, song_info["preview_url"], title=song_info["title"], performer=song_info["artist"], reply_to_message_id=message.id)

