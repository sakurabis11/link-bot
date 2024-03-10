from pyrogram import filters, Client
import time
import asyncio
import shlex
import math
from datetime import datetime
import os
from typing import Callable, Coroutine, Dict, List, Tuple, Union

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
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
    stark_cmd = f"ffmpeg -i {vid_path} -map 0:a friday.mp3"
    await runcmd(stark_cmd)
    final_warner = "friday.mp3"
    if not os.path.exists(final_warner):
        return None
    return final_warner

@Client.on_message(filters.command(["convert", "vid_to_aud"] ))
async def shazam_(client, message):
 try:
    stime = time.time()
    msg = await message.reply_text("`Shazaming This Song.")
    if not message.reply_to_message.video:
        return await msg.edit("`Reply To Audio File.`")
    if message.reply_to_message.video:
        video_file = await message.reply_to_message.download()
        music_file = await convert_to_audio(video_file)
        etime = time.time()
        t_k = round(etime - stime)
        await client.send_audio(message.chat.id, music_file)
        t_taken = await message.reply_text(f"<code>{t_k} Seconds</code>")
        await asyncio.sleep(10)
        await t_taken.delete()
    else:
        pass
 except Exception as e:
        await message.reply_text(f"{e}")
        os.remove(music_file)

