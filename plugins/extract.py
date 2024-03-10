import os
import shutil
import time
from datetime import datetime
from typing import Tuple

from pyrogram import filters, Client
from pyrogram.types import Message

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = cmd.split()
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

async def convert_to_audio(vid_path):
    stark_cmd = f"ffmpeg -i {vid_path} -map 0:a sd.mp3"
    _, _, returncode, _ = await runcmd(stark_cmd)
    final_warner = "sd.mp3"
    if not os.path.exists(final_warner) or returncode != 0:
        return None
    return final_warner

@Client.on_message(filters.command(["convert", "vid_to_aud"]))
async def shazam_(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.video:
            return await message.reply_text("Reply to a video...")
        stime = time.time()
        msg = await message.reply_text("Converting video to audio...")
        video_file = await message.reply_to_message.download()
        music_file = await convert_to_audio(video_file)
        if music_file is None:
            return await msg.edit("Failed to convert video to audio.")
        etime = time.time()
        t_k = round(etime - stime)
        await client.send_audio(message.chat.id, music_file)
        await msg.edit(f"<code>{t_k} Seconds for converting this video to audio...</code>")
        os.remove(video_file)
        os.remove(music_file)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
