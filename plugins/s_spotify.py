from pyrogram import Client, filters
import spotipy
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECERT

   # Create a Spotify API client instance
spotify = spotipy.Spotify(
    client_credentials_manager=spotipy.SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
    )
)

spotify_link_regex = re.compile(r"(https://open.spotify.com/track/\w+)")
   
@client.on_message(spotify_link_regex)
async def download_song(client, message):
       # Extract the song name from the message
       song_name = message.text

       # Search for the song on Spotify
       results = spotify.search(q=song_name, type="track")

       # Get the Spotify track ID
       track_id = results["tracks"]["items"][0]["id"]

       # Download the song in MP3 format
       song_url = spotify.track(track_id)["preview_url"]
       song_data = requests.get(song_url)

       # Send the song as MP3 file to the user
       client.send_audio(message.chat.id, song_data, title=song_name, performer="Spotify")
