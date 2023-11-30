import pyrogram
from spotipy import Spotify
import pafy
import requests

@Client.on_message(filters.command("spotify"))
async def spoti_command(client, message):

    # Get the song name from the message
    song_name = message.text.split(" ", 1)[1]

    # Search for the song on Spotify
    spotify = Spotify()
    results = spotify.search(q=song_name, type="track")

    # Get the first result
    track = results["tracks"]["items"][0]

    # Get the track name, artist, and URL
    track_name = track["name"]
    artist = track["artists"][0]["name"]
    track_url = track["external_urls"]["spotify"]

    # Download the song using pafy
    video = pafy.new(track_url)
    audio = video.getbestaudio()
    audio.download()

    # Send a message with the track information and link
    reply = f"Track: {track_name}\nArtist: {artist}\nURL: {track_url}"
    message.reply_text(text=reply)

    # Send the downloaded song file
    with open(audio.filename, "rb") as song_file:
        message.reply_audio(audio.filename, caption=track_name, duration=audio.duration)

    # Delete the downloaded song file
    import os
    os.remove(audio.filename)
