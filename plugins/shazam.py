import os
import re
import asyncio
import contextlib
import tempfile
import io
import requests
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

def recognize_song(audio_path):
    url = "https://api.musixmatch.com/ws/1.1/track.search"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    }
    with managed_bytes_io(open(audio_path, "rb").read(1024 * 1024)) as f:
        files = {"audio_file": f}
        response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()
    result = response.json()
    if result["message"]["header"]["status_code"] == 200:
        track = result["message"]["body"]["track_list"][0]
        return {
            "title": track["track"]["title"],
            "artist": track["track"]["artist_name"],
        }
    else:
        return None


@Client.on_message(filters.video | filters.audio)
async def shazam_command(client, message):
    if message.text.strip().lower() != "/shazam":
        return

    media_group = []
    if message.video:
        audio_path = await extract_audio(message.video)
        result = recognize_song(audio_path)
        if result:
            media_group.append(InputMediaAudio(audio_path, caption=f"{result['title']} - {result['artist']}"))
    elif message.audio:
        result = recognize_song(message.audio.file_path)
        if result:
            media_group.append(InputMediaAudio(message.audio.file_path, caption=f"{result['title']} - {result['artist']}"))

    if media_group:
        await client.send_media_group(message.chat.id, media_group)
    else:
        await client.send_message(message.chat.id, "Sorry, I couldn't recognize the song.")
