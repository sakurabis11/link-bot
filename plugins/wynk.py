
import asyncio
import os
import re
import sys
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

@Client.on_message(filters.command("wynk"))
async def wynk_download(client, message):

    song_name = message.text.split(" ", 1)[1]
    ydl_opts = {
        "format": "bestaudio",
        "noprogress": True,
        "quiet": True,
        "outtmpl": "%(title)s.%(ext)s",
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:

            search_result = ydl.extract_info("https://music.wynk.in/search/" + song_name, download=False)

            ydl.download([search_result["entries"][0]["url"]])

            await client.send_audio(
                message.chat.id,
                f"{search_result['entries'][0]['title']}.{search_result['entries'][0]['ext']}",
            )
        except Exception as e:
            await message.reply_text(f"Sorry, I couldn't download the song. Error: {e}")


