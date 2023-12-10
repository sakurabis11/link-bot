from pyrogram import Client, filters
import ffmpeg

@Client.on_message(filters.command("convert") & ~filters.edited)
async def convert_video_to_audio(client, message):
    # Check if reply is video
    if not message.reply_to_message or not message.reply_to_message.video:
        await message.reply_text("Please reply to a video to convert it to audio.")
        return

    # Download video
    video_path = await client.download_media(message.reply_to_message.video.file_id)

    # Extract audio
    audio_path = f"{video_path}.mp3"
    ffmpeg(inputs={video_path: None}, outputs={audio_path: None}).run()

    # Send audio
    await message.reply_audio(audio_path)

    # Delete files
    import os
    os.remove(video_path)
    os.remove(audio_path)
