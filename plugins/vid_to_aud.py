import asyncio
from pyrogram import Client, filters

async def convert_video_to_audio(client, message):
    try:
        video_file = message.document or message.video
        if not video_file:
            return await message.reply_text("Please send a video file to convert.")

        downloaded_file_path = await client.download_media(video_file.file_id)

        output_file_path = f"{downloaded_file_path[:-4]}.mp3" 
        await client.run_ffmpeg(
            input=downloaded_file_path, output=output_file_path, c="acodec libmp3lame"
        )

        await client.send_audio(message.chat.id, output_file_path)

        await client.delete_downloaded_file(downloaded_file_path)
        await client.delete_downloaded_file(output_file_path)

    except Exception as e:
        print(f"Error during conversion: {e}")
        await message.reply_text(f"An error occurred while converting the video: {e}")

@Client.on_message(filters.command("mp3") & filters.document | filters.video)
async def video_to_audio_handler(client, message):
    await convert_video_to_audio(client, message)
