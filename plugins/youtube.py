from pyrogram import Client, filters
import yt_dlp
from yt_dlp import YoutubeDL
import requests

@Client.on_message(filters.command("yt"))
async def download_video(client, message):
  try:
    command_parts = message.text.split(" ", 1)

    if len(command_parts) == 1:
      await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ ᴜʀʟ (e.g., /yt https://www.youtube.com/watch?v=2Vv-BfVoq4g&pp=ygUHcGVyZmVjdA%3D%3D)")
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
        downloading_message = await message.reply_text(f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ {video_title}...**")
        try:
          await downloading_message.delete(delay=10)
        except Exception as e:
          print(f"ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇ: {e}")

        ydl.download([url])

        duration_minutes = int(duration) // 60
        
        response = requests.get(thumbnail_url, stream=True)
        thumbnail_file = open("thumbnail.jpg", "wb")
        for chunk in response.iter_content(1024):
          thumbnail_file.write(chunk)
        thumbnail_file.close()

        try:
        
          await client.send_video(
            chat_id=message.chat.id,
            video=f"{video_title}.mp4",
            caption=f"ᴛɪᴛʟᴇ:**{video_title}**\n**ᴅᴜʀᴀᴛɪᴏɴ:** {duration_minutes} ᴍɪɴᴜᴛᴇs\n",
            thumb="thumbnail.jpg"  
          )
          await message.reply_text("ᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ")
        except Exception as e:
          print(f"ᴇʀʀᴏʀ sᴇɴᴅɪɴɢ ᴠɪᴅᴇᴏ: {e}")

      else:
        await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴛʀɪᴇᴠᴇ ᴠɪᴅᴇᴏ. ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴜʀʟ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.")

  except Exception as e:
    await message.reply_text(f"ᴇʀʀᴏʀ: {e}")
