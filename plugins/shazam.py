from pyrogram import Client, filters
from shazamio import Shazam
from pyrogram.types import Message, Voice, Audio, Video
import logging
import ffmpeg
import os
import datetime
import asyncio
from pyrogram.types import *
from pyrogram.errors import *

from utils import humanbytes

@Client.on_message(filters.command(["shazam"]))
async def shazam_handler(client, message):
    stime = time.time()

    reply_msg = await message.reply_text("Shazaming this song...")

    try:
        media_file, duration = await get_media_info(message.reply_to_message)
    except ValueError as e:
        return await reply_msg.edit(f"Error: {e}")

    try:
        thumb, song_info = await shazam_song(media_file, duration)
    except Exception as e:
        return await reply_msg.edit(f"Shazam failed: {e}")

    etime = time.time()
    time_taken = round(etime - stime)

    caption = format_caption(song_info, duration, time_taken)

    try:
        await reply_msg.edit(caption)
        if thumb:
            await message.reply_to_message.reply_photo(thumb, caption=caption, quote=True)
    except MessageNotModified:
        pass
    finally:
        cleanup_files(media_file, thumb)

async def get_media_info(message):
    if not message or not message.reply_to_message:
        raise ValueError("Reply to a valid message containing an audio or video file.")

    media = message.reply_to_message.audio or message.reply_to_message.voice or message.reply_to_message.video
    if not media:
        raise ValueError("Reply to an audio or video file.")

    media_file = await message.reply_to_message.download()
    duration = get_duration(media)

    return media_file, duration

async def shazam_song(media_file, duration):
    if duration <= 0:
        raise ValueError("Invalid duration of the media file.")

    thumb, by, title = await shazam(media_file)
    if title is None:
        raise ValueError("No results found.")

    return thumb, {"title": title, "by": by, "duration": duration, "size": os.stat(media_file).st_size}

def format_caption(song_info, duration, time_taken):
    size = humanbytes(song_info["size"])
    dur_str = str(datetime.timedelta(seconds=song_info["duration"]))

    caption = f"""<b><u>Shazamed Song</b></u>
<b>Song Name :</b> <code>{song_info['title']}</code>
<b>Singer :</b> <code>{song_info['by']}</code>
<b>Duration :</b> <code>{dur_str}</code>
<b>Size :</b> <code>{size}</code>
<b>Time Taken :</b> <code>{time_taken} Seconds</code>
<b><u>Shazamed By @YourShazamBot</b></u>"""

    return caption

def cleanup_files(*files):
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to remove file {file}: {e}")
