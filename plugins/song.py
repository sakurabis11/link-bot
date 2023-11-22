import pyrogram
from pyrogram import Client, filters, types
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWaitError
import yt_dlp
import os

DOWNLOAD_LOCATION = "downloads"  # Change this to your desired download location

@Client.on_message(filters.private)
def handle_message(message: types.Message):
    if message.text == "/start":
        keyboard = ReplyKeyboardMarkup(
            [[InlineKeyboardButton("Search Songs", callback_data="search_songs")]]
        )
        message.reply(
            "Welcome to the Telegram Song Downloader bot! 🎉\n\nUse the buttons below to search for songs and download them:",
            reply_markup=keyboard,
        )

    elif message.text.startswith("/search"):
        search_query = message.text.split(" ")[1]
        try:
            search_results = yt_dlp.YoutubeDL().extract_info(f"ytsearch:{search_query}", download=False)["entries"]

            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"🎵 {result['title']}", callback_data=f"download_song {result['url']}"
                        )
                    ]
                    for result in search_results[:10]
                ]
            )

            message.reply(
                "Choose the song you want to download:", reply_markup=reply_markup
            )
        except yt_dlp.utils.DownloadError:
            message.reply("No matching songs found.")


@Client.on_callback_query()
def handle_callback_query(callback_query: types.CallbackQuery):
    if callback_query.data.startswith("download_song"):
        song_url = callback_query.data.split(" ")[1]

        try:
            with yt_dlp.YoutubeDL({"format": "bestaudio/bestvideo[ext=m4a]/best[ext=mp4]"}) as ydl:
                video_info = ydl.extract_info(song_url, download=False)

                song_title = video_info["title"]
                song_format = ydl.prepare_filename(video_info)

                message = callback_query.message
                message.edit_text("Downloading song...")

                ydl.download([song_url])

                os.rename(song_format, f"{DOWNLOAD_LOCATION}/{song_title}.mp3")

                message.edit_text("Song downloaded successfully! 🎉\n\nDownload location: " + DOWNLOAD_LOCATION)

        except yt_dlp.utils.DownloadError:
            message.edit_text("Error downloading song. Please try again later.")


