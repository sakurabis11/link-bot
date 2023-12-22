import pyrogram
from pyrogram import filters, Client
import aiohttp
import os

@Client.on_message(filters.regex(r"https://open.spotify.com/track/(.*)"))
async def download_and_send(client, message):
    track_url = message.text
    user_id = message.from_user.id

    try:
        song_file = await download_track(track_url)
        try:
            await client.send_audio(user_id, audio=song_file, caption="Downloaded from Spotify")
            os.remove(song_file)  # Optional: Delete the file after sending
        except Exception as e:
            await client.send_message(user_id, "Failed to send audio: {}".format(e))
    except Exception as e:
        await client.send_message(user_id, "Failed to download track: {}".format(e))

async def download_track(track_url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(track_url)
        soup = BeautifulSoup(await response.text(), "html.parser")

        # Extract download link from HTML (replace with your specific logic)
        download_link = soup.find("a", class_="track-download-link").get("href")  # Example placeholder

        download_response = await session.get(download_link)
        song_file = open("downloaded_song.mp3", "wb")
        song_file.write(await download_response.read())
        song_file.close()

        return song_file
