import os
import logging
from pyrogram import Client, filters, enums
import requests
import json

@Client.on_message(filters.command("ringtune"))
async def music(client, message):
    # Extract the query from the command message
    query = " ".join(message.command[1:])

    # Check if a query is provided
    if not query:
        await client.message.send_message(message.chat.id, "Please provide a song name to search. Usage: /ringtune <song_name> or <song_name + artist_name>")
        return

    try:
        # Send a request to the Deezer API with the search query
        response = requests.get(f"https://api.deezer.com/search?q={query}")

        # Check if the request was successful
        response.raise_for_status()

        # Convert the response to JSON format
        result = response.json()

        # Check if there are any search results
        if "data" not in result or not result["data"]:
            await client.send_message(message.chat.id, "No results found for the given query.")
            return

        # Get the first result (most relevant result)
        song = result["data"][0]

        # Create a dictionary to store the song information
        song_info = {
            "artist": song["artist"]["name"],
            "title": song["title"],
            "duration": song["duration"],
            "preview_url": song["preview"],
        }

        # Send a message to the user with the song details and a download link
        await client.message.send_message(message.chat.id, f"Artist: {song_info['artist']}\nTitle: {song_info['title']}\nDuration: {song_info['duration']} seconds\nPreview: {song_info['preview_url']}")

        # Send chat action to indicate that the bot is uploading audio
        await client.send_chat_action(message.chat.id, "upload_audio")

        # Follow the redirect to get the actual audio URL
        stream = requests.get(song_info['preview_url'], stream=True)
        if stream.status_code == 200:
            # Download the audio data
            audio_data = stream.read()

            # Send the audio file using the downloaded data
            await client.send_audio(message.chat.id, audio_data, title=song_info['title'], performer=song_info['artist'], reply_to_message_id=message.id)
        else:
            await client.send_message(message.chat.id, "Failed to download the audio file. Please try again later.")
    except requests.RequestException as e:
        # Handle HTTP request errors
        logging.error(f"Error fetching song information: {e}")
        await client.send_message(message.chat.id, "An error occurred while fetching the song information. Please try again later.")
