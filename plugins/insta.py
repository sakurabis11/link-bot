import pyrogram
from pyrogram import Client, filters
from snapinsta import SnapInsta
import regex

@Client.on_message(filters.regex(r"https?://www.instagram.com/.*"))
def download_media(client, message):
    insta_url = message.text

    media_type = extract_media_type(insta_url)

    if media_type:
        snapinsta = SnapInsta()
        download_result = snapinsta.download_by_url(insta_url)

        if download_result.success:
            client.send_message(chat_id=message.chat.id, text=f"Downloaded {media_type} successfully!")
            client.send_document(chat_id=message.chat.id, document=download_result.file_path)
        else:
            client.send_message(chat_id=message.chat.id, text=f"Download failed: {download_result.error_message}")
    else:
        client.send_message(chat_id=message.chat.id, text="Invalid or unsupported Instagram URL.")

def extract_media_type(insta_url):
    # Implement regex patterns for matching media types
    media_types = {
        "reel": r"/reel/([^/]+)/?",
        "video": r"/tv/([^/]+)/?",
        "post": r"/p/([^/]+)/?",
        "story": r"/stories/([^/]+)/?",
    }
    for media_type, pattern in media_types.items():
        match = re.search(pattern, insta_url)
        if match:
            return media_type
    return None
  
