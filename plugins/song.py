import asyncio
import os
import re
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube
from youtube_search import YoutubeSearch

@Client.on_message(filters.command(["song"]))
async def download_song(client, message):
    # Check if the user has provided a song name
    if len(message.text.split()) < 2:
        await message.reply("Please provide the song name you want")
        return

    song_name = message.text.split()[1:]  # Extract the song name parts into a list
    song_name = " ".join(song_name)  # Combine the song name parts into a single string

    # Send "Searching..." message before searching
    await message.reply("⏳")

    # Search for the song on YouTube
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    if not search_results:
        await message.reply("No song found with that name")
        return

    song_url = search_results[0]["url_suffix"]
    song_title = search_results[0]["title"]
    duration = search_results[0]["duration"]

    try:
        yt = YouTube(f"https://www.youtube.com{song_url}")
        audio_streams = yt.streams.filter(only_audio=True)

        if not audio_streams:
            await message.reply("No audio stream found for the specified video")
            return

        video = audio_streams.first()
        audio_filename = f"{song_title}.mp3"

        try:
            video.download(filename=audio_filename)
            thumbnail_url = yt.thumbnail_url

            caption = f"** {song_title}**\n" + \
                       f" ᴅᴜʀᴀᴛɪᴏɴ: {duration}\n" + \
                       f" ʏᴏᴜ ᴛᴜʙᴇ: <a href='https://www.youtube.com{song_url}'>ʏᴏᴜ ᴛᴜʙᴇ</a>"

            await message.reply_audio(
                audio_filename,
                caption=caption,
                thumb=thumbnail_url,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴜᴘᴘᴏʀᴛ", url=S_CHANNEL
                            )
                        ]
                    ]
                )
            )
        except Exception as e:
            await message.reply(f"Failed to send with thumbnail and button: {e}")
            await message.reply_audio(audio_filename, caption=caption)  # Send without thumbnail/button

        finally:
            os.remove(audio_filename)  # Delete the downloaded song

    except Exception as e:
        await message.reply(f"Error downloading song: {e}")
