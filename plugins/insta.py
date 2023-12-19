import os
from pyrogram import Client, filters
from instaloader import Instaloader

L = Instaloader()

# Download and send reel function
def download_and_send_reel(client, chat_id, url):
    try:
        # Download reel with Instaloader
        post = L.context.get_media_by_url(url)
        video_path = post.download_video()
        caption = post.caption

        # Open video file in binary mode
        with open(video_path, "rb") as f:
            video_data = f.read()

        # Send video as document
        client.send_document(chat_id, video_data, document_name="reel.mp4")

        # Send caption (optional)
        if caption:
            client.send_message(chat_id, caption)

        # Delete downloaded file
        os.remove(video_path)
    except Exception as e:
        client.send_message(chat_id, f"Error downloading reel: {e}")


@Client.on_message(filters.regex(r"(https://www.instagram.com/.*)"))
async def reel_handler(client, message):
    url = message.match.group(1)
    if url.startswith("https://www.instagram.com/reel/"):
        download_and_send_reel(client, message.chat_id, url)
    else:
        # Handle non-reel content (optional)
        # You can choose to ignore non-reel URLs,
        # provide a message informing the user,
        # or even attempt to download other types of content (e.g., photos)
        client.send_message(message.chat_id, "This URL isn't an Instagram reel. Please send a valid reel URL.")

