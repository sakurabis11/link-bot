from pyrogram import Client, filters
from pytube import YouTube

@Client.on_message(filters.command("ytv"))
async def download_video(client, message):
  try:
    # Extract the YouTube URL from the message text
    url = message.text.split(" ")[1]

    # Download the video using pytube
    yt = YouTube(url)
    video = yt.streams.first()
    video.download()

    # Upload the downloaded video to the user
    await client.send_video(message.chat.id, video.filename, caption=f"Downloaded video from: {url}")

    # Delete the downloaded file
    os.remove(video.filename)
  except Exception as e:
    await client.send_message(message.chat.id, f"Error downloading video: {e}")

