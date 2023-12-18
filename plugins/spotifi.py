import os
from pyrogram import Client, filters
from spotipy import Spotify
from spotdl import SpotifyDownloader
import ffmpeg
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

spotify = Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:8888/callback",
  ))

@Client.on_message(filters.command("spot"))
async def handle_spot_command(client, message):
  # Extract the Spotify link from the message
  spotify_url = message.text.split()[1]

  # Use the Spotify API to get info about the song/playlist
  try:
    info = spotify.track(spotify_url) if "/track/" in spotify_url else spotify.playlist(spotify_url)
  except Exception as e:
    message.reply_text(f"Error: {e}")
    return

  try:
    downloader = SpotifyDownloader(spotify_url)
    audio_data = downloader.download()
    message.reply_audio(audio_data)
  except Exception as e:
    message.reply_text(f"Error downloading with Spotdl: {e}")
    # Added error message and fallback
    message.reply_text("Falling back to preview URL due to download error.")

   audio_url = info["tracks"]["items"][0]["track"]["preview_url"]

   try:
        with open("song.mp3", "wb") as f:
            f.write(ffmpeg.output(audio_url, None)["data"])
    except Exception as e:
        message.reply_text(f"Error downloading with ffmpeg: {e}")
        message.reply_text("Consider using alternative download methods.")

   message.reply_audio(open("song.mp3", "rb").read())

   os.remove("song.mp3")
