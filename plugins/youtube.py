from pyrogram import Client, filters
import yt_dlp

@Client.on_message(filters.command("yt"))
async def download_video(client, message):
  try:
    url = message.text.split(" ", 1)[1]

    ydl_opts = {
      'outtmpl': '%(title)s.%(ext)s',
      'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Choose best format
      'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'
      }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info_dict = ydl.extract_info(url, download=False)
      video_title = info_dict.get('title', None)

      await message.reply_text(f"Downloading {video_title}...")

      ydl.download([url])

      # Send the downloaded video using the correct argument:
      await message.reply_video(video=f"{video_title}.mp4")  # Corrected argument

      await message.reply_text("Video downloaded and sent!")

  except Exception as e:
    await message.reply_text(f"Error: {e}")
