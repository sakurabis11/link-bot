import os
from pyrogram import Client, filters
from spotipy.oauth2 import SpotifyClientCredentials


# Initialize Spotify client
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    )
)



@Client.on_message(filters.regex(r"/track (.*)"))
async def send_song(client, message):
    song_name = message.matches[0][1]
    try:
        results = sp.search(q=song_name, type="track", limit=1)
        track_uri = results["tracks"]["items"][0]["uri"]
        track_info = sp.track(track_uri)
        audio_file = await sp.audio_features(track_uri)[0]["preview_url"]
        await message.reply_audio(audio_file)
    except IndexError:
        await message.reply("Song not found.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

