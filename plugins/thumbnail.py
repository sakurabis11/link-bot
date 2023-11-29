# code from MRMKN, it also includes some improvements such as: os.path.exists(), os.makedirs()
from pyrogram import Client, filters
from info import ADMINS
import os

import os

# Define the download location
DOWNLOAD_LOCATION = "thumbnails"

@Client.on_message(filters.private & filters.command("set_thumbnail") & filters.user(ADMINS))
async def set_tumb(bot, msg):       
    if len(dir) == 0:
        await client.download_media(message=msg.photo.file_id, file_name=f"{DOWNLOAD_LOCATION}/thumbnail.jpg")
        return await msg.reply(f"Your permanent thumbnail is saved in dictionary ✅️ \nif you change yur server or recreate the server app to again reset your thumbnail⚠️")            
    else:    
        os.remove(f"{DOWNLOAD_LOCATION}/thumbnail.jpg")
        await client.download_media(message=msg.photo.file_id, file_name=f"{DOWNLOAD_LOCATION}/thumbnail.jpg")               
        return await msg.reply(f"Your permanent thumbnail is saved in dictionary ✅️ \nif you change yur server or recreate the server app to again reset your thumbnail⚠️")  


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
