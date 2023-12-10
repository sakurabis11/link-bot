from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Define your client id and client secret
client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET

# Initialize Spotify OAuth
scope = "playlist-read-private,playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, scope=scope))

# Download options
ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


@Client.on_message(filters.command("spotify"))
async def handle_spotify_command(client, message):
    # Check if message contains Spotify URL
    if "open.spotify.com" in message.text:
        spotify_url = message.text.split(" ", 1)[1]
        try:
            # Extract song information from Spotify URL
            track_info = sp.track(spotify_url)

            # Send song information and thumbnail
            thumbnail = track_info["album"]["images"][0]["url"]
            await client.send_photo(message.chat.id, thumbnail)
            track_info_str = f"{track_info['name']} by {track_info['artists'][0]['name']} on {track_info['album']['name']}"
            await client.send_message(message.chat.id, track_info_str)

            # Download and send song
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(track_info["external_urls"]["spotify"], download=False)
                ydl.download([info["id"]])
                await client.send_audio(message.chat.id, f"{info['title']}.mp3")
        except Exception as e:
            # Handle any errors during Spotify URL processing
            await client.send_message(message.chat.id, f"Error extracting information from Spotify URL: {e}")
    else:
        # Handle normal query if no Spotify URL
        query = message.text.split(" ", 1)[1]
        try:
            # Search for songs on Spotify
            results = sp.search(q=query, type="track", limit=5)
            if len(results["tracks"]["items"]) == 0:
                # Inform user if no results found
                await client.send_message(message.chat.id, "No results found.")
                return

            # Send song information and thumbnails for each result
            for i, track in enumerate(results["tracks"]["items"]):
                thumbnail = track["album"]["images"][0]["url"]
                await client.send_photo(message.chat.id, thumbnail)
                track_info = f"{i+1}. {track['name']} by {track['artists'][0]['name']} on album {track['album']['name']}"
                await client.send_message(message.chat.id, track_info)

            # Wait for user selection
            user_choice = await client.listen(filters.text & filters.reply_to(message), timeout=60)
            if not user_choice:
                # Inform user if no selection within timeout
                await client.send_message(message.chat.id, "Timed out. Please try again.")
                return

            # Get chosen track based on user selection
            chosen_track = results["tracks"]["items"][int(user_choice.text) - 1]

            # Download and send chosen song
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(chosen_track["external_urls"]["spotify"], download=False)
                ydl.download([info["id"]])
                await client.send_audio(message.chat.id, f"{info['title']}.mp3")
        except Exception as e:
            # Make sure this line is indented one level further
            await client.send_message(message.chat.id, f"Error: {e}")
