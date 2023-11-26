import os
import logging
from pyrogram import Client, filters
import requests
import json

logging.basicConfig(level=logging.INFO)

GROUP_CHAT_ID = "-1001568397419"

@Client.on_message(filters.text & filters.group(GROUP_CHAT_ID))
async def song(client, message):
    query = message.text

    # Send a request to the Deezer API with the search query
    response = requests.get(f"https://api.deezer.com/search?q={query}")

    # Convert the response to JSON format
    result = response.json()

    # Get the first result (most relevant result)
    song = result["data"][0]

    # Get the song details
    artist = song["artist"]["name"]
    title = song["title"]
    duration = song["duration"]
    preview_url = song["preview"]

    # Send a message to the user with the song details and a download link
    client.send_message(message.chat.id, f"Artist: {artist}\nTitle: {title}\nDuration: {duration} seconds\nPreview: {preview_url}")

    # Send a chat action to indicate that the bot is uploading an audio file
    client.send_chat_action(message.chat.id, "upload_audio")

    # Send the audio file to the user
    client.send_audio(message.chat.id, preview_url, title=title, performer=artist)
