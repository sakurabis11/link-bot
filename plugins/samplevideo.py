import os
import time
import pyrogram
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_writer import FFMPEGWriter

# Define command handler for generating sample videos
@Client.on_message(pyrogram.filters.command("generate_sample", prefixes=["/"]))
async def generate_sample_video(client, message):
    try:
        # Check if a movie file is provided
        if message.reply_to_message is not None and message.reply_to_message.document is not None:
            movie_file = message.reply_to_message.document
            movie_filename = movie_file.file_name

            # Download the movie file
            download_path = f"movie_samples/{movie_filename}"
            if not os.path.exists(download_path):
                client.download_media(message.reply_to_message)
                time.sleep(2)

            # Generate sample video clip
            sample_duration = 480  # Set sample duration to 8 minutes (480 seconds)
            sample_clip = VideoFileClip(download_path).subclip(0, sample_duration)

            # Write sample video to file
            sample_filename = f"sample_{movie_filename}"
            sample_clip.write_videofile(f"movie_samples/{sample_filename}", writer="ffmpeg")

            # Send sample video as a reply
            client.send_video(message.chat.id, f"movie_samples/{sample_filename}")
        else:
            raise Exception("Please reply to a movie file with /generate_sample")
    except Exception as e:
        client.send_message(message.chat.id, f"Error: {e}")

