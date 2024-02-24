import pyrogram
import requests
from pyrogram import filters, Client

def shazam_recognize(audio_file):
    """Performs Shazam recognition on an audio file."""
    url = "https://api.safone.dev/shazam"
    files = {"audio_file": audio_file}

    try:
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raise error for non-200 status codes
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API request: {e}")
        return None  # Indicate error

    return response.json()

@Client.on_message(filters.command(["shazam"]))
async def handle_shazam_command(client, message):
    """Handles the Shazam command and replies with recognized song information."""

    if not message.reply_to_message:
        await message.reply_text("Please reply to an audio or video message to use Shazam.")
        return

    reply_message = message.reply_to_message

    if reply_message.audio:
        media_type = "audio"
        media_id = reply_message.audio.file_id
    elif reply_message.video:
        media_type = "video"
        media_id = reply_message.video.file_id
    else:
        await message.reply_text("Unsupported media type. Please reply to an audio or video message.")
        return

    try:
        audio_file = await client.download_media(media_id)

        response = shazam_recognize(audio_file)

        if response:
            shazam_results = response["tracks"]["hits"]

            if shazam_results:
                top_result = shazam_results[0]
                artist_name = top_result["artist"]["name"]
                song_title = top_result["track"]["title"]

                await message.reply_text(f"Shazam results for {media_type}:\nArtist: {artist_name}\nSong: {song_title}")
            else:
                await message.reply_text("Sorry, Shazam couldn't recognize the song.")
        else:
            await message.reply_text("An error occurred during Shazam recognition.")
    except requests.exceptions.RequestException as e:
        await message.reply_text(f"An error occurred: {e}")
    except Exception as e:
        await message.reply_text(f"Unexpected error: {e}")
    finally:
        audio_file.close()  # Ensure audio file is closed properly

