import pyrogram
from pyrogram import filters, Client
from pyrogram.types import Message
import yt_dlp

async def generate_thumbnail(video_path):
    """Generates a thumbnail from the video using OpenCV."""
    import cv2

    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    cv2.imwrite("thumbnail.jpg", image)  # Save as JPEG

@Client.on_message(filters.command("do"))
async def download_video(client, message):
    link = message.text.split(" ", 1)[1]

    ydl_opts = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "writethumbnail": True,  # Extract thumbnail using yt-dlp
        "writesubtitles": True,  # Optional: Download subtitles
        # Add other yt-dlp options as needed (refer to documentation)
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info_dict)
            await message.reply_text(f"Downloading video: {filename}")

            # Generate thumbnail if not extracted by yt-dlp
            if not info_dict.get("thumbnail", None):
                await generate_thumbnail(filename)

            # Send video and thumbnail (or generated thumbnail)
            with open(filename, "rb") as video_file:
                await message.reply_video(video_file, caption="Downloaded video", thumb="thumbnail.jpg")

            # Optional: Send subtitles if downloaded
            subtitles_file = f"downloads/{info_dict['title']}.{info_dict['subtitles'][0]['ext']}"
            if subtitles_file:
                await message.reply_document(subtitles_file, caption="Subtitles")

        except Exception as e:
            await message.reply_text(f"Error downloading video: {e}")


