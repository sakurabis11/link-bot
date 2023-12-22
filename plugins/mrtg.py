import pyrogram
from pyrogram import filters, Client
import aiohttp  # Import aiohttp for asynchronous requests
from bs4 import BeautifulSoup
import os

@Client.on_message(filters.regex(r"https://open.spotify.com/track/(.*)"))
async def download_and_send(client, message):
    track_url = message.text
    user_id = message.from_user.id

    try:
        song_file = await download_track(track_url)
        try:
            await client.send_audio(user_id, audio=song_file, caption="Downloaded from Spotify")
            # Delete the file after sending (optional)
            os.remove(song_file)
        except Exception as e:
            await client.send_message(user_id, "Failed to send audio: {}".format(e))
    except Exception as e:
        await client.send_message(user_id, "Failed to download track: {}".format(e))

async def download_track(track_url):
    # Replace with your preferred Spotify download method
    # Ensure it complies with Spotify's Terms of Service

    async with aiohttp.ClientSession() as session:  # Create an asynchronous session
        response = await session.get(track_url)  # Await the asynchronous response
        soup = BeautifulSoup(await response.text(), "html.parser")  # Parse the HTML

        # ... (Extract download link from the HTML using appropriate methods)

        download_response = await session.get(download_link)  # Await the download response
        song_file = open("downloaded_song.mp3", "wb")
        song_file.write(await download_response.read())  # Write the content to the file
        song_file.close()

    return song_file
