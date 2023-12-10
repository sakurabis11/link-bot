from pyrogram import Client, filters
from spotipy.oauth2 import SpotifyOAuth
from yt_dlp import YoutubeDL
from info import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Spotify client ID and client secret
client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET

# Initialize Spotify OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret))

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
    query = message.text.split(" ", 1)[1]
    try:
        results = sp.search(q=query, type="track", limit=5)
        if len(results["tracks"]["items"]) == 0:
            client.send_message(message.chat.id, "No results found.")
            return
        
        # Send song information and thumbnails
        for i, track in enumerate(results["tracks"]["items"]):
            thumbnail = track["album"]["images"][0]["url"]
            client.send_photo(message.chat.id, thumbnail)
            track_info = f"{i+1}. {track['name']} by {track['artists'][0]['name']} on album {track['album']['name']}"
            client.send_message(message.chat.id, track_info)

        # Wait for user selection
        user_choice = client.listen(filters.text & filters.reply_to(message), timeout=60)
        if not user_choice:
            client.send_message(message.chat.id, "Timed out. Please try again.")
            return

        chosen_track = results["tracks"]["items"][int(user_choice.text) - 1]

        # Download and send song
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(chosen_track["external_urls"]["spotify"], download=False)
            
            ydl.download([info["id"]])
            client.send_audio(message.chat.id, f"{info['title']}.mp3")
    except Exception as e:
        client.send_message(message.chat.id, f"Error: {e}")


app.run()
