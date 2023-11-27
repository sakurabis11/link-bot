import os
import logging
import requests
from pyrogram import Client, filters, enums
from info import API_ID, API_HASH, BOT_TOKEN, PORT

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.text)
async def song(client, message):
    # Extract the search query from the message
    query = message.text.strip()

    # Construct the Deezer API search URL
    api_url = f"https://api.deezer.com/search?q={query}"

    # Send a GET request to the Deezer API
    try:
        response = requests.get(api_url)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing Deezer API: {e}")
        await client.send_message(message.chat.id, "Error accessing Deezer API.")
        return

    # Check if the API request was successful
    if response.status_code != 200:
        logging.error(f"Deezer API returned error code: {response.status_code}")
        await client.send_message(message.chat.id, "Error accessing Deezer API.")
        return

    # Parse the JSON response
    result = response.json()

    # Check if there are any search results
    if "data" not in result or not result["data"]:
        await client.send_message(message.chat.id, "No results found.")
        return

    # Extract the first search result (most relevant result)
    song = result["data"][0]

    # Extract song details
    artist = song["artist"]["name"]
    title = song["title"]
    duration = song["duration"]
    preview_url = song["preview"]

    # Download the audio file from the preview URL
    try:
        audio_file_path = f"temp/{title}.mp3"
        with open(audio_file_path, "wb") as f:
            f.write(requests.get(preview_url).content)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading audio file: {e}")
        await client.send_message(message.chat.id, "Error downloading song.")
        return

    # Send song details and download link to the user
    message_text = f"**Song:** {title}\n**Artist:** {artist}\n**Duration:** {duration} seconds\n**Preview:** {preview_url}"
    await client.send_message(message.chat.id, message_text)

    # Send chat action indicating uploading audio file
    await client.send_chat_action(message.chat.id, "upload_audio")

    # Send the audio file to the user
    await client.send_audio(message.chat.id, audio=audio_file_path, title=title, performer=artist)

    # Delete the downloaded audio file
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)
