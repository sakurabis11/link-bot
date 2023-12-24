from pyrogram import Client, filters
import yt_dlp
from yt_dlp import YoutubeDL
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
      thumbnail_url = info_dict.get('thumbnail', None)  # Get thumbnail URL

      if video_title and thumbnail_url:
        downloading_message = await message.reply_text(f"**Downloading {video_title}...**")
        try:
          await downloading_message.delete(delay=10)
        except Exception as e:
          print(f"Failed to delete message: {e}")

        ydl.download([url])

        # Convert duration to minutes
        duration_minutes = int(duration) // 60

        # Download the thumbnail
        response = requests.get(thumbnail_url, stream=True)
        thumbnail_file = open("thumbnail.jpg", "wb")
        for chunk in response.iter_content(1024):
          thumbnail_file.write(chunk)
        thumbnail_file.close()

        try:
          # Send video and thumbnail as a single message using client.send_video
          await client.send_video(
            chat_id=message.chat.id,
            video=f"{video_title}.mp4",
            caption=f"**Title:** {video_title}\n**Duration:** {duration_minutes} minutes\n",
            thumb="thumbnail.jpg"  # Attach the downloaded thumbnail
          )
          await message.reply_text("Upload completed")
        except Exception as e:
          print(f"Error sending video: {e}")

      else:
        await message.reply_text("Unable to retrieve video title or thumbnail. Please check the video URL and try again.")

  except Exception as e:
    await message.reply_text(f"Error: {e}")
