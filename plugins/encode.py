import os
import subprocess
from pyrogram import Client, filters
import ffmpeg

@Client.on_message(filters.document | filters.video)
async def encode_file(client, message):
    file_name = message.document.file_name or message.video.file_name
    file_path = await message.download()

    if file_name.lower().endswith(('.mkv', '.mp4')):
        try:
            output_file_path = f"output_{file_name}"
            subprocess.run([
                "ffmpeg", "-i", file_path, "-c:v", "libx264", "-crf", "23", output_file_path
            ], check=True)

            await message.reply_document(output_file_path)

            os.remove(file_path)
            os.remove(output_file_path)

        except subprocess.CalledProcessError as e:
            await message.reply_text("Encoding failed: {}".format(e))

        else:
            await message.reply_text("File encoded successfully!")

    else:
        await message.reply_text("Unsupported file format. Please send an MKV or MP4 file.")
