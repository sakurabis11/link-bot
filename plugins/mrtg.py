import pyrogram
from pyrogram import Client, filters

# Function to download and send song
async def download_song(link, chat_id):
    try:
        song = spotifydownload.download_song(link)
        with open(song.file_path, "rb") as f:
            await client.send_audio(chat_id, f, title=song.title, performer=song.artist)
    except Exception as e:
        await client.send_message(chat_id, f"Error downloading song: {e}")

# Handle Spotify links
@Client.on_message(filters.regex(r"https://open.spotify.com/(track|album|playlist)/(\w+)"))
async def handle_spotify_link(client, message):
    await download_song(message.text, message.chat.id)

