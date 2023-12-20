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

    # Attempt to download the reel video using the appropriate method
    try:
      video_filename = f"reel_{reel_id}.mp4"

      # Replace 'download_reels' with the correct method based on your Instaloader version
      # Refer to the Instaloader documentation for guidance
      insta_loader.download_post(reel_id, target=video_filename)  # Example assuming the correct method is 'download_post'

      await message.reply_video(video=video_filename, supports_streaming=True)
    except Exception as e:
      await message.reply_text(f"Error downloading the reel: {str(e)}")
  else:
    await message.reply_text("Invalid link format. Please provide a valid Instagram reel link.")
