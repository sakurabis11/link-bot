import pyrogram
from pyrogram import filters, Client
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os

SPOTIFY_CLIENT_ID = "21cf39f58bf7494d8fa377c59b72211c"
SPOTIFY_CLIENT_SECRET = "cc98f5a4038e40a9adc7573bf5b072a5"

# Initialize Pyrogram client and Spotify API
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri="http://://localhost:27017",
        scope="user-read-playback-state,user-modify-playback-state"
    )
)

# Define function to download a song from Spotify URL
def download_song(spotify_url):
    # Extract song ID from URL
    song_id = spotify_url.split("/")[-1]

    # Get song information
    song_info = sp.track(song_id)

    # Download song using spotipy-dl
    if os.path.exists(song_info["name"] + ".mp3"):
        send_message("Song already downloaded: " + song_info["name"] + ".mp3")
        return

    output_file = requests.get(os.path.join("https://spdle.com/api", song_id)).content
    with open(song_info["name"] + ".mp3", "wb") as f:
        f.write(output_file)

    send_message("Song downloaded successfully: " + song_info["name"] + ".mp3")

# Define handler for the `/spotify` command
@Client.on_message(filters.command(["spotify"]))
def download_command(client, message):
    if len(message.command) == 2:
        spotify_url = message.command[1]
        download_song(spotify_url)
    else:
        send_message("Invalid usage. Send `/download` followed by the Spotify URL")

# Define function to send messages to the user
def send_message(message_text):
    client.send_message(message.chat.id, message_text)
