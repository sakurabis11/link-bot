import pyrogram
import aiohttp
import requests
import logging
from pyrogram import filters, Client

# Safone.dev API endpoint
API_ENDPOINT = "https://api.safone.dev/shazam"

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

async def identify_audio_video(client, message, chat_id):
    try:
        # Download audio/video file
        file_id = message.audio.file_id if message.audio else message.video.file_id
        audio_video_bytes = await client.download_file(file_id)

        # Prepare request data
        data = {
            "audio_file": (audio_video_bytes, "audio.mp3"),  # Adjust filename and extension if needed
            "additional_info": "optional_info"  # Add any user-provided info
        }

        async with aiohttp.ClientSession() as session:
            # Send API request with rate limiting
            async with session.post(API_ENDPOINT, data=data) as response:
                if response.status == 200:
                    # Parse response and send bot message
                    recognition_data = await response.json()
                    recognition_message = f"Identified: {recognition_data['title']} by {recognition_data['artist']} (Link: {recognition_data['link']})"
                    await client.send_message(chat_id, recognition_message)
                else:
                    error_message = f"API error: {response.status} - {await response.text()}"
                    logging.error(error_message)
                    await client.send_message(chat_id, "An error occurred. Please try again later.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await client.send_message(chat_id, "An unexpected error occurred. Please try again later.")


@Client.on_message(filters.command("shazam"))
async def shazam_command(client, message):
    chat_id = message.chat.id
    if message.audio or message.video:
        await identify_audio_video(client, message, chat_id)
    else:
        await client.send_message(chat_id, "Please send an audio or video file.")
