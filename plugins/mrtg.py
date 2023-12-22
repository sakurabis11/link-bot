import pyrogram
from pyrogram import filters, Client
import aiohttp 
import re
import requests
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
            os.remove(song_file)
        except Exception as e:
            await client.send_message(user_id, "Failed to send audio: {}".format(e))
    except Exception as e:
        await client.send_message(user_id, "Failed to download track: {}".format(e))

async def download_track(track_url):
    async with aiohttp.ClientSession() as session: 
        response = await session.get(track_url) 
        soup = BeautifulSoup(await response.text(), "html.parser")  

        download_response = await session.get(download_link)
        song_file = open("downloaded_song.mp3", "wb")
        song_file.write(await download_response.read())
        song_file.close()

    return song_file
