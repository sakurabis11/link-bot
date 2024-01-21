import pyrogram
from pyrogram import filters, Client
from pyrogram.types import Message
from bs4 import BeautifulSoup
import requests


@Client.on_message(filters.command("lyrics"))
async def get_lyrics(client, update):
    message = update.message
    chat_id = message.chat.id

    # Get the song title and artist from the message
    song_title = message.text.split(" ")[1]
    artist = message.text.split(" ")[2]

    # Make an HTTP request to the musiXmatch API to get the lyrics
    url = f"https://api.musixmatch.com/ws/1.1/track.lyrics.get?q_track={song_title}&q_artist={artist}&apikey={lyrics_api_key}"
    response = requests.get(url)

    # Parse the JSON response and get the lyrics
    if response.status_code == 200:
        response_data = response.json()
        lyrics = response_data["message"]["body"]["lyrics"]["lyrics_body"]

        # Send the lyrics to the user
        await client.send_message(chat_id, lyrics)
    else:
        await client.send_message(chat_id, f"Error: Unable to find lyrics for '{song_title}' by '{artist}'")

