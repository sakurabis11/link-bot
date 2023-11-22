import pyrogram
import yt_dlp‎
from pyrogram import types, Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.utils import get_file_id, download_media
from info import API_ID, API_HASH, BOT_TOKEN

# Define the command handler for downloading songs
@Client.on_message(filters.command("download"))
async def download_song(client, message):
    # Get the song name from the message
    song_name = message.text.split()[1]

    # Search for the song on YouTube
    youtube_results = search(song_name)

    # If no results found, notify the user
    if not youtube_results:
        message.reply_text("No results found for the song '" + song_name + "'")
        return

    # Send a message with the first YouTube result and a download button
    first_result = youtube_results[0]
    message.reply_text(f"Found the song '{first_result['title']}' by {first_result['artist']} on YouTube.\nDo you want to download this song?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download", callback_data=first_result['url'])]]))

# Define the callback handler for handling download requests
@Client.on_callback_query()
async def handle_download_request(client, callback_query):
    # Get the song URL from the callback data
    song_url = callback_query.data

    # Download the song from YouTube
    audio = download_song_from_youtube(song_url)

    # Send the downloaded song to the user
    callback_query.message.reply_document(audio)

# Define a function to download songs from YouTube
def download_song_from_youtube(song_url):
    # Extract the video ID from the URL
    video_id = song_url.split("v=")[1]

    # Download the audio file
    audio_file = youtube_dl.YoutubeDL({"format": "bestaudio/best"})
    audio_file.download([song_url])
    audio_filename = audio_file.prepare_filename(info_dict={})

    # Return the audio file path
    return audio_filename
