from pyrogram import Client, filters
from pytube import YouTube
import os


@Client.on_message(filters.command("ytv"))
async def download_video(client, message):
    try:
        # Get video URL from message
        url = message.text.split(" ")[1]

        # Download video using pytube
        yt = YouTube(url)

        # Get best available video format
        video = yt.streams.filter(progressive=True, only_audio=False).order_by('resolution').desc().first()

        # Create temporary video filename with extension
        filename = f"{yt.title}.{video.extension}"

        # Download video and update progress
        video.download(filename=filename, progress_hook=lambda chunk, file_handle, bytes_remaining: update_message(client, message, bytes_remaining))

        # Upload video with caption
        await client.send_video(message.chat.id, filename, caption=f"Downloaded video from: {url}")

        # Delete downloaded file
        os.remove(filename)
    except Exception as e:
        # Handle different exceptions with specific messages
        if isinstance(e, KeyError):
            await client.send_message(message.chat.id, f"Invalid video format.")
        elif isinstance(e, OSError):
            await client.send_message(message.chat.id, f"Error writing video file.")
        else:
            await client.send_message(message.chat.id, f"Error downloading video: {e}")

def update_message(client, message, bytes_remaining):
    # Update download progress message
    remaining_mb = round(bytes_remaining / 1048576, 2)
    await client.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"Downloading... (Remaining: {remaining_mb} MB)")


