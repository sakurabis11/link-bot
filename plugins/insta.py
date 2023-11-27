import asyncio
import os
import requests
from pyrogram import Client, filters, enums
from info import API_ID, API_HASH, BOT_TOKEN, PORT

# Initialize Pyrogram Client
app = Client("instagram-downloader")

# Define command handler for downloading posts
@app.on_message(filters.command("download_post"))
async def download_post(_, message):
    # Check if post URL is provided
    if not message.reply_to_message or not message.reply_to_message.text:
        await app.send_message(message.chat.id, "Please reply to a message with an Instagram post URL")
        return

    # Extract post URL
    post_url = message.reply_to_message.text

    # Download post media
    try:
        response = requests.get(post_url)
        if response.status_code != 200:
            raise Exception("Failed to download post media")

        # Extract media type (image or video)
        media_type = response.headers["Content-Type"].split("/")[0]

        # Determine media path based on media type
        media_path = os.path.join("downloads", f"{post.shortcode}{'.' if media_type == 'image' else '.mp4'}")

        # Save media content to file
        with open(media_path, "wb") as f:
            f.write(response.content)

        # Send downloaded media
        if media_type == "image":
            await app.send_photo(message.chat.id, media_path)
        else:
            await app.send_video(message.chat.id, media_path)

        # Remove temporary media file
        os.remove(media_path)
    except Exception as e:
        await app.send_message(message.chat.id, f"Error downloading post: {e}")

# Define command handler for downloading reels
@Client.on_message(filters.command("download_reel"))
async def download_reel(_, message):
    # Check if reel URL is provided
    if not message.reply_to_message or not message.reply_to_message.text:
        await app.send
