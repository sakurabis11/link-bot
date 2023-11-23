import os, asyncio
import aiohttp
from pyrogram import Client, filters
from telegraph import upload_file
from utils import get_file_id


@Client.on_message(filters.command("telegraph"))
async def telegraph_upload(bot, update):
    # Check if the user has replied to a message
    replied = update.reply_to_message
    if not replied:
        await update.reply_text("Reply To A Photo Or Video Under 15mb")
        return

    # Get the file information from the replied message
    file_info = get_file_id(replied)
    if not file_info:
        await update.reply_text("Not Supported!")
        return

    # Send a message indicating that the file is being downloaded
    download_text = await update.reply_text(
        text="<code>Downloading To My Server ...</code>", disable_web_page_preview=True
    )

    # Download the media from the replied message
    media = await update.reply_to_message.download()

    # Update the message to indicate that the file has been downloaded
    await download_text.edit_text(
        text="<code>Downloading Completed. Now I am Uploading to telegra.ph Link ...</code>",
        disable_web_page_preview=True,
    )

    # Upload the media to Telegraph
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await download_text.edit_text(
            text=f"Error :- {error}", disable_web_page_preview=True
        )
        return

    # Remove the downloaded media file if possible
    try:
        os.remove(media)
    except Exception as error:
        print(error)

    # Send the Telegraph link and upload speed information to the user
    await download_text.edit_text(
        text=f"https://telegra.ph{response[0]}",
        disable_web_page_preview=True,
    )
