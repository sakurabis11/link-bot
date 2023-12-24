from pyrogram import Client, filters, InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

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
           duration = info_dict.get('duration', None)  # Retrieve video duration

           if video_title:
               downloading_message = await message.reply_text(f"**Downloading {video_title}...**")
               try:
                   await downloading_message.delete(delay=10)
               except Exception as e:
                   print(f"Failed to delete message: {e}")

               ydl.download([url])

               video_path = f"{video_title}.mp4"
               caption = f"**Title:** {video_title}\n**Duration:** {duration}"

               if message.chat.type == "group":  # Handle group requests
                   keyboard = InlineKeyboardMarkup(
                       [
                           [
                               InlineKeyboardButton(
                                   text="Get Video in PM",
                                   callback_data="send_video_pm"
                               )
                           ]
                       ]
                   )
                   await message.reply_video(video=video_path, caption=caption, reply_markup=keyboard)
               else:  # Send directly in private chats
                   await message.reply_video(video=video_path, caption=caption)

               await message.reply_text("ᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ")
           else:
               await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴛʀɪᴇᴠᴇ ᴠɪᴅᴇᴏ ᴛɪᴛʟᴇ. ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴜʀʟ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.")

   except Exception as e:
       await message.reply_text(f"ᴇʀʀᴏʀ: {e}")

   @Client.on_callback_query()
   async def handle_callback(client, callback_query):
       if callback_query.data == "send_video_pm":
           video_path = f"{callback_query.message.caption.splitlines()[1].split('**Title:** ')[1]}.mp4"
           await client.send_video(callback_query.from_user.id, video=video_path, caption=callback_query.message.caption)
           await callback_query.answer("Video sent to your PM!")
