import pyrogram
import re
import instaloader
from pyrogram import Client, filters
from pyrogram.types import *

# Create an instance of Instaloader
insta_loader = instaloader.Instaloader()

@Client.on_message(filters.regex(r"https://www\.instagram\.com/reel/(.*)"))
async def extract_reel_link(client, message):
    link = message.text

    if "https://www.instagram.com/reel/" in link:
        reel_id = link.replace("https://www.instagram.com/reel/", "").split("/")[0]

        # Download the reel video
        try:
            video_filename = f"reel_{reel_id}.mp4"
            insta_loader.download_reels(reel_id, target=video_filename)

            # Send the video to the user
            await message.reply_video(video=video_filename, supports_streaming=True)
        except Exception as e:
            await message.reply_text(f"Error downloading the reel: {str(e)}")
    else:
        await message.reply_text("Invalid link format. Please provide a valid Instagram reel link.")

