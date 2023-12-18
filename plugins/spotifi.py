# Import necessary libraries
import pyrogram
from pyrogram.types import Message
from spotipy import Spotify
import subprocess
import ffmpeg

spotify = Spotify(auth_manager=SpotifyOAuth())


# Define command handler for "/spotifi"
@Client.on_message(filters.command("spotifi"))
async def handle_spotify_command(client: Client, message: Message):
        # Extract link and song name from message
        link, song_name = message.text.split()[1:]

        # Download song using spotipy
        try:
            song_data = spotify.track(link)
            song_file = spotify.track_to_file(link, filename=f"{song_name or song_data['name']}.mp3")

            # Send downloaded song or error message
            if song_file:
                try:
                    # Convert MP3 to Opus (optional)
                    subprocess.run(["ffmpeg", "-i", song_file, "-c:a", "libopus", "-b:a", "64k", "output.opus"])
                    converted_file = open("output.opus", "rb")
                    client.send_audio(message.chat.id, converted_file, title=song_name or song_data["name"])
                except Exception as e:
                    # Fallback to sending MP3 if Opus conversion fails
                    client.send_audio(message.chat.id, song_file, title=song_name or song_data["name"])
            else:
                client.send_message(message.chat.id, "Error downloading song!")
        except Exception as e:
            client.send_message(message.chat.id, f"Error: {e}")
