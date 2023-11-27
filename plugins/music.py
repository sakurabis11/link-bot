import os
import logging
from pyrogram import Client, filters
import requests
import json

# Define the command handler for /song
@Client.on_message(filters.command("music"))
async def music(client, message):
    # Extract the query from the command message
    query = " ".join(message.command[1:])
    
    # Check if a query is provided
    if not query:
        client.send_message(message.chat.id, "Please provide a song name to search. Usage: /music <song_name>")
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
            client.send_message(message.chat.id, "No results found for the given query.")
            return

        # Get the first result (most relevant result)
        song = result["data"][0]

        # Get the song details
        artist = song["artist"]["name"]
        title = song["title"]
        duration = song["duration"]
        preview_url = song["preview"]

        # Send a message to the user with the song details and a download link as a reply to the original message
        client.send_message(
            message.chat.id,
            f"Artist: {artist}\nTitle: {title}\nDuration: {duration} seconds\nPreview: {preview_url}",
            reply_to_message_id=message.message_id
        )

        # Send chat action to indicate that the bot is uploading audio
        client.send_chat_action(message.chat.id, "upload_audio")

        # Send the audio preview to the user as a reply to the original message
        client.send_audio(message.chat.id, preview_url, title=title, performer=artist, reply_to_message_id=message.message_id)
        
    except requests.RequestException as e:
        # Handle HTTP request errors
        logging.error(f"Error fetching song information: {e}")
        client.send_message(message.chat.id, "Error fetching song information. Please try again later.")
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        logging.error(f"Error decoding JSON response: {e}")
        client.send_message(message.chat.id, "Error decoding JSON response from Deezer API. Please try again later.")
    except Exception as e:
        # Handle other unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
        client.send_message(message.chat.id, "An unexpected error occurred. Please try again later.")
