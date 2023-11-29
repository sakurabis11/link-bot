# code from MRMKN, it also includes some improvements such as: os.path.exists(), os.makedirs()
from pyrogram import Client, filters
from info import ADMINS
import os

import os

# Define the download location
DOWNLOAD_LOCATION = "thumbnails"

@Client.on_message(filters.private & filters.command("set_thumbnail") & filters.user(ADMINS))
async def set_thumbnail(client, message):
    # Create the download directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)

    # Check if a thumbnail already exists
    thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)

    # Check if the message contains a photo
    if msg.photo is None:
        await msg.reply_text("Please send a photo to set as the thumbnail.")
        return

    # Download the thumbnail
    await client.download_media(message=msg.photo.file_id, file_name=thumbnail_path)

    # Remove filters from the photo (optional)
    # msg.photo.filters.clear()

    # Send confirmation message
    await msg.reply_text("Your permanent thumbnail has been saved ✅️")


@Client.on_message(filters.private & filters.command("view_thumbnail") & filters.user(ADMINS))
async def view_thumbnail(bot, msg):
    if not os.path.exists(f"{DOWNLOAD_LOCATION}/thumbnail.jpg"):
        await msg.reply_text(text="You don't have any thumbnail")
        return

    # Send the thumbnail
    await msg.reply_photo(photo=f"{DOWNLOAD_LOCATION}/thumbnail.jpg", caption="This is your current thumbnail")

@Client.on_message(filters.private & filters.command(["del_thumbnail", "remove_thumbnail"]) & filters.user(ADMINS))
async def delete_thumbnail(client, msg):
    if not os.path.exists(f"{DOWNLOAD_LOCATION}/thumbnail.jpg"):
        await msg.reply_text(text="You don't have any thumbnail")
        return

    # Delete the thumbnail
    os.remove(f"{DOWNLOAD_LOCATION}/thumbnail.jpg")

    # Send confirmation message
    await msg.reply_text("Your thumbnail was removed🚫")
