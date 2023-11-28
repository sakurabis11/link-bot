# code from MRMKN, it also includes some improvements such as: os.path.exists(), os.makedirs()
from pyrogram import Client, filters
from info import ADMIN, DOWNLOAD_LOCATION
import os

@Client.on_message(filters.private & filters.command("set_thubnail") & filters.user(ADMIN))
async def set_thumbnail(client, msg):
    if not os.path.exists(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)

    # Check if a thumbnail already exists
    if os.path.exists(f"{DOWNLOAD_LOCATION}/thumbnail.jpg"):
        os.remove(f"{DOWNLOAD_LOCATION}/thumbnail.jpg")

    # Download the new thumbnail
    await bot.download_media(message=msg.photo.file_id, file_name=f"{DOWNLOAD_LOCATION}/thumbnail.jpg")

    # Remove filters from the photo
    msg.photo.filters.clear()

    # Send confirmation message
    await msg.reply_text(
        f"Your permanent thumbnail is saved in dictionary ✅️ \nIf you change your server or recreate the server app, the thumbnail will be reset⚠️"
    )

@Client.on_message(filters.private & filters.command("view_thumbnail") & filters.user(ADMIN))
async def view_thumbnail(bot, msg):
    if not os.path.exists(f"{DOWNLOAD_LOCATION}/thumbnail.jpg"):
        await msg.reply_text(text="You don't have any thumbnail")
        return

    # Send the thumbnail
    await msg.reply_photo(photo=f"{DOWNLOAD_LOCATION}/thumbnail.jpg", caption="This is your current thumbnail")

@Client.on_message(filters.private & filters.command(["del_thumbnail", "remove_thumbnail"]) & filters.user(ADMIN))
async def delete_thumbnail(client, msg):
    if not os.path.exists(f"{DOWNLOAD_LOCATION}/thumbnail.jpg"):
        await msg.reply_text(text="You don't have any thumbnail")
        return

    # Delete the thumbnail
    os.remove(f"{DOWNLOAD_LOCATION}/thumbnail.jpg")

    # Send confirmation message
    await msg.reply_text("Your thumbnail was removed🚫")
