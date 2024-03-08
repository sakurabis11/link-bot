import asyncio
import random
from pyrogram import Client, filters

MOTIVATION_CHANNEL_ID = -1001943067765  # Use a negative value for channel IDs

@Client.on_message(filters.command("motivation"))
async def send_random_motivation_video(client, message):
    try:
        # Get a list of all video messages in the motivation channel
        async for video in client.get_chat_history(MOTIVATION_CHANNEL_ID, filter=filters.video):
            videos.append(video)  # Store video messages in a list

        if not videos:
            await message.reply_text("No motivational videos found in the channel.")
            return

        # Select a random video from the list
        random_video = random.choice(videos)

        # Forward the random video to the user
        await message.reply_video(random_video.video.file_id)

    except Exception as e:
        print(f"Error occurred: {e}")
        await message.reply_text("An error occurred while sending the video.{e}")

videos = []


