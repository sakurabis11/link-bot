from pyrogram import Client, filters
import ffmpeg 
import os
import time, datetime
from os import environ,execl
from sys import executable

async def convert_to_audio(vid_path):
    stark_cmd = f"ffmpeg -i {vid_path} -map 0:a friday.mp3"
    await runcmd(stark_cmd)
    final_warner = "friday.mp3"
    if not os.path.exists(final_warner):
        return None
    return final_warner

@Client.on_message(filters.command("audio"))
async def aud(client, message):
    stime = time.time()
    msg = await message.reply_text("`Converting This Video to Audio.")
    if not message.reply_to_message:
        return await msg.edit("`Reply To Video File`")
    if not message.reply_to_message.video:
        return await msg.edit("`Reply To Audio File.`")
    video_file = await message.reply_to_message.download()
    music_file = await convert_to_audio(video_file)
    etime = time.time()
    await client.send_audio(message.chat.id, music_file)
    os.remove(music_file)
