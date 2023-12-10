from pyrogram import Client, filters
from instaloader import Profile, Post, Instaloader
from pyrogram.types import Message
import os

@Client.on_message(filters.command("insta"))
async def download_media(client: Client, message: Message):
    # Extract link from the message
    link = message.text.split(" ")[1]

    # Check if link is valid
    try:
        # Identify media type
        media = Post.from_url(link)

        # Check media type and download accordingly
        if media.is_video:
            video_path = media.download_video()
            await client.send_video(message.chat.id, video_path)
        elif media.is_photo:
            photo_path = media.download_photo()
            await client.send_photo(message.chat.id, photo_path)
        else:
            # Handle unsupported media type
            await message.reply_text(f"Unsupported media type: {media.type}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

    # Delete downloaded files if they exist
    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(photo_path):
        os.remove(photo_path)
