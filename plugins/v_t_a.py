import os
import re
import asyncio
import contextlib
import tempfile
import io
from pyrogram import Client, filters

async def extract_audio(video):
    temp_dir = tempfile.TemporaryDirectory()
    audio_path = os.path.join(temp_dir.name, "audio.mp3")
    await ffmpeg_extract_audio(audio_path, video)
    return audio_path

@contextlib.contextmanager
def managed_bytes_io(data):
    result = io.BytesIO(data)
    try:
        yield result
    finally:
        result.close()

def ffmpeg_extract_audio(audio_path, video):
    process = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-i", video,
        "-vn",
        audio_path,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await process.wait()

@Client.on_message(filters.video & filters.duration(less_than="00:05:00"))
async def extract_video_command(client, message):
    await client.send_message(message.chat.id, "Extracting audio from the video...")
    video_path = await client.download_media(message)
    audio_path = await extract_audio(video_path)
    await client.send_audio(message.chat.id, audio_path)
    await client.delete_messages(message.chat.id, [message.message_id])

