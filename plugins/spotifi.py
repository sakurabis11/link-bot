import os
import requests
from pyrogram import Client, filters
import re

spotify_filter = filters.regex(pattern=r"https://open.spotify.com/track/(.*)")

@Client.on_message(spotify_filter)
async def process_spotify_link(client, message):
    link = message.text
    track_id = link.split("/")[-1]

    try:
        response = requests.get(f"https://spotifymate.com/api/download?track_id={track_id}")
        response.raise_for_status()  # Raise an error for non-200 status codes
        download_url = response.json()["url"]

        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            filename = f"{track_id}.mp3"
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        try:
            await message.reply_audio(filename)
            os.remove(filename)  # Remove the downloaded file
        except Exception as e:
            await message.reply_text(f"Error sending audio: {e}")
    except Exception as e:
        await message.reply_text(f"Error downloading song: {e}")


