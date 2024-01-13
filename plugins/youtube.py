python
import asyncio
import pyrogram
from pyrogram.enums import ParseMode
from pyrogram.raw import functions, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch

# Initialize the Pyrogram client
client = pyrogram.Client("my_bot", api_id=12345, api_hash="abcdef")

# Define callback query handler
@client.on_callback_query()
async def callback_query_handler(client, callback_query):
    # Get the data from the callback query
    data = callback_query.data

    # Check if the data is a YouTube URL
    if data.startswith("https://www.youtube.com/"):
        # Get the video ID from the URL
        video_id = data.split("=")[1]

        # Download the video and audio files
        video_file = await download_video(video_id)
        audio_file = await download_audio(video_id)

        # Send the video and audio files to the user
        await client.send_video(callback_query.message.chat.id, video_file, caption="Here's the video you requested.", reply_to_message_id=callback_query.message.id)
        await client.send_audio(callback_query.message.chat.id, audio_file, caption="Here's the audio you requested.", reply_to_message_id=callback_query.message.id)
    else:
        # The data is not a YouTube URL, so send an error message to the user
        await client.send_message(callback_query.message.chat.id, "Invalid YouTube URL. Please send a valid URL.", reply_to_message_id=callback_query.message.id)

# Define function to download YouTube video
async def download_video(video_id):
    # Use youtube-dl to download the video
    video_file = f"{video_id}.mp4"
    await asyncio.get_running_loop().run_in_executor(None, lambda: youtube_dl.YoutubeDL().download(f"https://www.youtube.com/watch?v={video_id}", output=video_file))
    return video_file

# Define function to download YouTube audio
async def download_audio(video_id):
    # Use youtube-dl to download the audio
    audio_file = f"{video_id}.mp3"
    await asyncio.get_running_loop().run_in_executor(None, lambda: youtube_dl.YoutubeDL({'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}).download(f"https://www.youtube.com/watch?v={video_id}", output=audio_file))
    return audio_file


