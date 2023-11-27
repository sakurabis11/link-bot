import os
import logging
from pyrogram import Client, filters, enums
import requests
import json

# Define the command handler for /song
@Client.on_message(filters.command("ringtune"))
async def music(client, message):
    # Extract the query from the command message
    query = " ".join(message.command[1:])

    # Check if a query is provided
    if not query:
        await client.send_message(message.chat.id, "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ sᴏɴɢ ɴᴀᴍᴇ ᴛᴏ sᴇᴀʀᴄʜ. ᴜsᴀɢᴇ: /ringtune <song_name> or <song_name + Artist_name>")
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
            await client.send_message(message.chat.id, "ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ ғᴏʀ ᴛʜᴇ ɢɪᴠᴇɴ {query}.")
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
        await client.send_message(message.chat.id, f"ʜᴇʏ {message.from_user.mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ {query}\n\n◐ᴀʀᴛɪsᴛ: {song_info['artist']}\n◐ᴛɪᴛʟᴇ: {song_info['title']}\n◐ᴅᴜʀᴀᴛɪᴏɴ: {song_info['duration']} sᴇᴄᴏɴᴅs\n\nʏᴏᴜ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜɪs sᴏɴɢ ғʀᴏᴍ ᴄʜʀᴏᴍᴇ: {song_info['preview_url']}")

        # Send chat action to indicate that the bot is uploading audio
        await client.send_chat_action(message.chat.id, "upload_audio")

        # Check if the message is a reply to another audio message
        if message.reply_to_message and message.reply_to_message.media:
            # If it is, send the audio preview as a reply to the original audio message
            await client.send_audio(message.chat.id, song_info['preview_url'], title=song_info['title'], performer=song_info['artist'], reply_to_message_id=message.reply_to_message.id)
        else:
            # Otherwise, send it as a reply to the original message
            await client.send_audio(message.chat.id, song_info['preview_url'], title=song_info['title'], performer=song_info['artist'], reply_to_message_id=message.id)
    except requests.RequestException as e:
        # Handle HTTP request errors
        logging.error(f"Error fetching song information: {e}")
        await client.send_message(message.chat.id, "An error occurred while fetching the song information. Please try again later.")
