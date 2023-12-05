from pyrogram import Client, filters 
from info import ADMINS, DOWNLOAD_LOCATION
import os

@Client.on_message(filters.private & (filters.photo | filters.command("view")) & filters.user(ADMINS))
async def handle_thumb(client, msg):
    if msg.photo:
        # Download and save thumbnail
        await bot.download_media(message=msg.photo.file_id, file_name=f"{DOWNLOAD_LOCATION}/thumbnail.jpg")
        return await msg.reply(f"Your permanent thumbnail is saved in dictionary ✅️ \nIf you change your server or recreate the server app to again reset your thumbnail⚠️")
    else:
        # Try to view thumbnail
        try:
            await msg.reply_photo(photo=f"{DOWNLOAD_LOCATION}/thumbnail.jpg", caption="This is your current thumbnail")
        except FileNotFoundError:
            return await msg.reply_text(text="You don't have any thumbnail")
        except Exception as e:
            print(e)
            return await msg.reply_text(text="Something went wrong while viewing your thumbnail.")

@Client.on_message(filters.private & filters.command(["del", "del_thumb"]) & filters.user(ADMINS))
async def del_tumb(client, msg):
    try:
        if os.path.exists(f"{DOWNLOAD_LOCATION}/thumbnail.jpg"):
            os.remove(f"{DOWNLOAD_LOCATION}/thumbnail.jpg")
            await msg.reply_text("Your thumbnail was removed")
        else:
            await msg.reply_text("No thumbnail found to delete.")
    except Exception as e:
        print(e)
        return await msg.reply_text(text="Something went wrong while deleting your thumbnail.")
