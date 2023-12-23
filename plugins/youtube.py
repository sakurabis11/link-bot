from pyrogram import Client, filters
import yt_dlp

@Client.on_message(filters.command("yt"))
async def download_video(client, message):
    try:
        command_parts = message.text.split(" ", 1)

        if len(command_parts) == 1:
            await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ ᴜʀʟ (ᴇɢ:- /yt https://www.youtube.com/watch?v=2Vv-BfVoq4g&pp=ygUHcGVyZmVjdA%3D%3D)")
            return

        url = command_parts[1]

        ydl_opts = {  # Removed extra indentation here
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

            if video_title:  # Check if title is available
                # Send the "Downloading..." message with scheduled deletion:
                downloading_message = await message.reply_text(f"**Downloading {video_title}...**")
                try:
                    await downloading_message.delete(delay=10)  # Schedule deletion after 10 seconds
                except Exception as e:
                    print(f"Failed to delete message: {e}")  # Log any deletion errors

                ydl.download([url])

                # Send the downloaded video with the caption:
                await message.reply_video(video=f"{video_title}.mp4", caption=video_title)  # Added caption

                await message.reply_text("ᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ")
            else:
                await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴛʀɪᴇᴠᴇ ᴠɪᴅᴇᴏ ᴛɪᴛʟᴇ. ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴜʀʟ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.")

    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ: {e}")
