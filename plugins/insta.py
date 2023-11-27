import asyncio
import os
import requests
from pyrogram import Client, filters, enums

# Define command handler for downloading posts
@Client.on_message(filters.command("download_post"))
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

        media_path = os.path.join("downloads", post.shortcode + ".jpg")

        with open(media_path, "wb") as f:
            f.write(response.content)

        # Send downloaded media
        await app.send_photo(message.chat.id, media_path)
        os.remove(media_path)
    except Exception as e:
        await app.send_message(message.chat.id, f"Error downloading post: {e}")

# Define command handler for downloading reels
@Client.on_message(filters.command("download_reel"))
async def download_reel(_, message):
    # Check if reel URL is provided
    if not message.reply_to_message or not message.reply_to_message.text:
        await app.send_message(message.chat.id, "Please reply to a message with an Instagram reel URL")
        return

    # Extract reel URL
    reel_url = message.reply_to_message.text

    # Download reel video
    try:
        response = requests.get(reel_url)
        if response.status_code != 200:
            raise Exception("Failed to download reel video")

        video_path = os.path.join("downloads", reel.shortcode + ".mp4")

        with open(video_path, "wb") as f:
            f.write(response.content)

        # Send downloaded video
        await app.send_video(message.chat.id, video_path)
        os.remove(video_path)
    except Exception as e:
        await app.send_message(message.chat.id, f"Error downloading reel: {e}")

