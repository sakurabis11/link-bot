import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define the bot command handler
@Client.on_message(filters.command("download"))
async def download_spotify_track(client, message):
    # Extract Spotify link from message text
    spotify_link = message.text.split()[1]

    # Validate Spotify link format
    if not spotify_link.startswith("https://open.spotify.com/"):
        await message.reply_text("Invalid Spotify link. Please provide a valid Spotify track URL.")
        return

    # Download Spotify track using yt-dlp
    async with app.get_chat(message.chat.id) as chat:
        await chat.send_message("Downloading track...")

        # Download process using asyncio
        process = await asyncio.create_subprocess_shell(f"yt-dlp -F 'best[audio/mp4]+best[audio/webm]+best[audio/ogg]' {spotify_link}")
        stdout, stderr = await process.communicate()

        # Check for errors
        if stderr:
            await chat.send_message(f"Error: {stderr.decode('utf-8')}")
            return

        # Extract audio information from stdout
        audio_info = stdout.decode('utf-8').split('\n')
        audio_filename = audio_info[-1].split('Destination: ')[1]

        # Send downloaded audio file
        await chat.send_document(audio_filename)

