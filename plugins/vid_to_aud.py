import os
import subprocess
import ffmpeg
from pyrogram import Client, filters

FFMPEG_PATH = "/usr/bin/ffmpeg"  

async def convert_to_audio(vid_path):
    command = f"ffmpeg -i {vid_path} -map 0:a obanai.mp3"
    process = await asyncio.create_subprocess(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_msg = stderr.decode("utf-8")
        return f"Error converting video: {error_msg}"

    if not os.path.exists("obanai.mp3"):
        return "Failed to generate audio file."

    return "obanai.mp3"


@Client.on_message(filters.command("audio"))
async def aud(client, message):
    stime = time.time()
    msg = await message.reply_text("`Converting This Video to Audio.`")
    if not message.reply_to_message:
        return await msg.edit("`Reply To Video File`")
    if not message.reply_to_message.video:
        return await msg.edit("`Reply To Audio File.`")

    video_file = await message.reply_to_message.download()
    music_file = await convert_to_audio(video_file)

    if isinstance(music_file, str) and music_file.startswith("Error"):
        await msg.edit(music_file)
        return

    etime = time.time()
    await client.send_audio(message.chat.id, music_file)
    os.remove(music_file)
    await msg.edit(f"Converted video to audio in {etime - stime:.2f} seconds.")
