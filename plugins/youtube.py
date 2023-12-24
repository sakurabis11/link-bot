from pyrogram import Client, filters
import yt_dlp
from info import S_CHANNEL
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests

@Client.on_message(filters.command("yt"))
async def download_video(client, message):
  try:
    command_parts = message.text.split(" ", 1)

    if len(command_parts) == 1:
      await message.reply_text("Please provide YouTube video URL (e.g., /yt https://www.youtube.com/watch?v=2Vv-BfVoq4g&pp=ygUHcGVyZmVjdA%3D%3D)")
      return

    url = command_parts[1]

    ydl_opts = {
      'outtmpl': '%(title)s.%(ext)s',
      'format': 'bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/best[height<=?720][ext=mp4]/best',  # Prioritize 720p
      'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'
      }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info_dict = ydl.extract_info(url, download=False)
      video_title = info_dict.get('title', None)
      duration = info_dict.get('duration', None)  # Get video duration

      if video_title:
        downloading_message = await message.reply_text(f"**Downloading {video_title}...**")
        try:
          await downloading_message.delete(delay=10)
        except Exception as e:
          print(f"Failed to delete message: {e}")

        ydl.download([url])

        # Convert duration to minutes
        duration_minutes = int(duration) // 60

        # Create inline keyboard for support channel
        support_button = [
          InlineKeyboardButton("Support Channel", url=S_CHANNEL)
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(support_button, n_cols=1))  # Adjust n_cols as needed

        # Send the downloaded video with caption and inline keyboard
        await message.reply_video(
          video=f"{video_title}.mp4",
          caption=f"**Title:** {video_title}\n**Duration:** {duration_minutes} minutes\n",
          reply_markup=reply_markup
        )

        await message.reply_text("Upload completed")
      else:
        await message.reply_text("Unable to retrieve video title. Please check the video URL and try again.")

  except Exception as e:
    await message.reply_text(f"Error: {e}")
