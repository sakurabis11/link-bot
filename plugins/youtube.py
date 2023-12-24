from pyrogram import Client, filters
import yt_dlp
from PIL import Image  # Import for thumbnail generation

@Client.on_message(filters.command("yt"))
async def download_video(client, message):
  try:
    command_parts = message.text.split(" ", 1)

    if len(command_parts) == 1:
      await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ ᴜʀʟ (ᴇɢ:- /yt https://www.youtube.com/watch?v=2Vv-BfVoq4g&pp=ygUHcGVyZmVjdA%3D%3D)")
      return

    url = command_parts[1]

    ydl_opts = {
      'outtmpl': '%(title)s.%(ext)s',
      'format': 'bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/best[height<=?720][ext=mp4]/best',
      'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'
      }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info_dict = ydl.extract_info(url, download=False)
      video_title = info_dict.get('title', None)

      if video_title:
        downloading_message = await message.reply_text(f"**Downloading {video_title}...**")
        try:
          await downloading_message.delete(delay=10)
        except Exception as e:
          print(f"Failed to delete message: {e}")

        ydl.download([url])

        # Generate thumbnail from the downloaded video:
        thumbnail_file = f"{video_title}_thumb.jpg"
        Image.open(f"{video_title}.mp4").save(thumbnail_file, "JPEG")  # Extract a JPEG thumbnail

        # Send the video with the generated thumbnail:
        await message.reply_video(video=f"{video_title}.mp4", thumb=thumbnail_file, caption=video_title)

        await message.reply_text("ᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ")
      else:
        await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴛʀɪᴇᴠᴇ ᴠɪᴅᴇᴏ ᴛɪᴛʟᴇ. ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴜʀʟ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.")

  except Exception as e:
    await message.reply_text(f"ᴇʀʀᴏʀ: {e}")
