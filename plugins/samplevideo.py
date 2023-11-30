import pyrogram
from pyrogram import filters, Client
from moviepy.editor import *
import os
import time
import random

@Client.on_message(filters.command("generatesamplevideo"))
def generatesamplevideo(client, message):
    if message.document or message.video:
        if message.document:
            media = message.document
        else:
            media = message.video

        download_path = client.download_media(media)

        try:
            video = VideoFileClip(download_path)
        except Exception as e:
            client.send_message(message.chat.id, f"Error: {e}")
            return

        filename = str(time.time()) + ".mp4"
        duration = random.uniform(0, 480)  # Random duration up to 8 minutes (480 seconds)
        sample_video = video.subclip(0, duration)
        sample_video.write_videofile(filename)
        client.send_video(message.chat.id, filename)
        os.remove(filename)
    else:
        client.send_message(message.chat.id, "Please send a document or video to generate a sample video.")
