from pyrogram import Client, filters
from shazamio import Shazam
from pyrogram.types import Message, Voice, Audio, Video
import logging
import ffmpeg
import os
import datetime
import asyncio
shazam = Shazam()

@Client.on_message(filters.command(["shazam", "whatsong"]))
async def shazam_handler(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply("Please reply to the audio or video message you want to Shazam.")
        return

    reply_message = message.reply_to_message
    media_type = reply_message.media

    if isinstance(media_type, (Voice, Audio)):
        # Extract audio from voice/audio message
        await message.reply("Downloading audio...")
        audio_bytes = await client.download_media(reply_message)
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
        video_path = await client.download_media(reply_message)
        audio_path = f"{video_path}.mp3"
        await message.edit_text("Converting video to audio...")
        await client.run(f"ffmpeg -i {video_path} -vn -ar 44100 -ac 2 {audio_path}")

        # Recognize song using Shazam
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        await message.edit_text("Analyzing audio...")
        recognition = shazam.recognize_song(audio_bytes)

        # Cleanup temporary files
        await client.run(f"rm {video_path} {audio_path}")

        if recognition:
            await message.edit_text(f"**Song:** {recognition.track.title} by {recognition.artist.name}")
        else:
            await message.edit_text("Sorry, I couldn't recognize the song.")

    else:
        await message.reply("Please reply to an audio or video message.")



