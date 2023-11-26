import os
import logging
from pyrogram import Client, filters
import requests

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command("ringtone") & filters.text)
async def song(client, message):
    query = message.text

    # Send a request to the Deezer API with the search query
    try:
        response = requests.get(f"https://api.deezer.com/search?q={query}")
    except requests.exceptions.RequestException as e:
        await client.send_message(message.chat.id, "Error accessing the API: " + str(e))
        return

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response to JSON format
        result = response.json()

        # Check if there are any search results
        if "data" in result and result["data"]:
            # Get the first result (most relevant result)
            song = result["data"][0]

            # Get the song details
            artist = song["artist"]["name"]
            title = song["title"]
            duration = song["duration"]

            # Send a message to the user with the song details and a download link
            await client.send_message(message.chat.id, "🎧 Downloading your ringtone...")

            # Download the audio file
            audio_url = song["preview"]
            audio_data = requests.get(audio_url).content

            # Send the audio file as a reply
            await client.send_audio(message.chat.id, audio_data, reply_to_message_id=message.chat.id, title=title, performer=artist)

            # Send a download complete message
            await client.send_message(message.chat.id, "✅ Download complete! Enjoy your new ringtone!")
        else:
            await client.send_message(message.chat.id, "No results found.")
    else:
        await client.send_message(message.chat.id, "Error accessing the API. Please try again later.")
