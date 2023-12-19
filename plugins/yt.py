from pyrogram import Client, InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube

# Audio qualities and corresponding bitrates
audio_qualities = {
    "Highest (320 kbps)": "320",
    "High (256 kbps)": "256",
    "Medium (192 kbps)": "192",
    "Low (128 kbps)": "128",
}

@Client.on_message(filters.command("yt"))
async def handle_message(client, message):
        video_link = message.text.split(" ")[1]

        # Validate link
        if not YouTube.is_valid_url(video_link):
            await message.reply("Invalid YouTube link!")
            return

        # Get video information
        try:
            video = YouTube(video_link)
        except Exception as e:
            await message.reply(f"Error fetching video: {e}")
            return

        # Create inline keyboard with audio quality options
        keyboard = InlineKeyboardMarkup()
        for name, bitrate in audio_qualities.items():
            button = InlineKeyboardButton(name, f"download_{bitrate}")
            keyboard.add_button(button)

        # Send message with keyboard
        await message.reply(f"Choose audio quality for '{video.title}':", reply_markup=keyboard)

@Client.on_callback_query()
async def handle_callback_query(client, query):
    # Get callback data and split into command and bitrate
    command, bitrate = query.data.split("_")

    # Download audio with selected bitrate
    try:
        audio_stream = video.streams.filter(only_audio=True, bitrate=bitrate).first().download()
        downloaded_file = f"{video.title}_{bitrate}.mp3"
        audio_stream.to_file(downloaded_file)
    except Exception as e:
        await query.answer(f"Error downloading audio: {e}")
        return

    # Send downloaded audio file
    await query.answer("Download successful!")
    await client.send_audio(query.message.chat.id, downloaded_file)

    # Delete downloaded file
    os.remove(downloaded_file)
