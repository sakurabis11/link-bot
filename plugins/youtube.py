import pyrogram
from pyrogram import Client, filters
import yt_dlp

@Client.on_message(filters.regex(r"https?://(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-_]*)(&(amp;)?[\w\?=]*)?"))
async def download_video(client, message):
    try:
        url = message.text
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'writethumbnail': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_file = ydl.prepare_filename(info_dict)
            ydl.download([url])

            await message.reply_video(video_file, thumb=info_dict.get("thumbnail"))

        # Remove downloaded file
        os.remove(video_file)

    except Exception as e:
        await message.reply_text(f"Error downloading video: {str(e)}")


