from pyrogram import Client, filters
from shazam import Shazam
from pyrogram.types import Message, Voice, Audio, Video
import logging

shazam = Shazam()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@Client.on_message(filters.command(["shazam"]))
async def shazam_handler(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply("Please reply to the audio or video message you want to Shazam.")
        return

    reply_message = message.reply_to_message
    media_type = reply_message.media

    if isinstance(media_type, (Voice, Audio)):
        # Extract audio from voice/audio message
        await message.reply("Downloading audio...")
        try:
            audio_bytes = await client.download_media(reply_message)
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            await message.edit_text("Error downloading audio. Please try again.")
            return
        await message.edit_text("Analyzing audio...")

        # Recognize song using Shazam
        recognition = shazam.recognize_song(audio_bytes)

        if recognition:
            await message.edit_text(f"**Song:** {recognition.track.title} by {recognition.artist.name}")
        else:
            await message.edit_text("Sorry, I couldn't recognize the song.")

    elif isinstance(media_type, Video):
        # Extract audio from video using ffmpeg
        await message.reply("Extracting audio...")
        try:
            video_path = await client.download_media(reply_message)
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            await message.edit_text("Error downloading video. Please try again.")
            return
        audio_path = f"{video_path}.mp3"

        try:
            await message.edit_text("Converting video to audio...")
            await client.run(f"ffmpeg -i {video_path} -vn -ar 44100 -ac 2 {audio_path}")
        except Exception as e:
            logger.error(f"Error converting video to audio: {e}")
            await message.edit_text("Error converting video to audio. Please try again.")
            return

        # Recognize song using Shazam
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        await message.edit_text("Analyzing audio...")
        recognition = shazam.recognize_song(audio_bytes)

        # Cleanup temporary files
        try:
            await client.run(f"rm {video_path} {audio_path}")
        except Exception as e:
            logger.error(f"Error cleaning up files: {e}")

        if recognition:
            await message.edit_text(f"**Song:** {recognition.track.title} by {recognition.artist.name}")
        else:
            await message.edit_text("Sorry, I couldn't recognize the song.")

    else:
        await message.reply("Please reply to an audio or video message.")

