# code from MRMKN, it also includes some improvements such as: try-except,os.listdir(),os.remove().
import time, os

from os import environ

from pyrogram import Client, filters, enums
from info import ADMINS
from utils import progress_message, humanbytes

CAPTION = environ.get("CAPTION", "{file_name}\n\n💽 size : {file_size}")

DOWNLOAD_LOCATION = "./DOWNLOADS"


@Client.on_message(filters.private & filters.command("rename") & filters.user(ADMINS))
async def rename_file(client, msg):
    reply = msg.reply_to_message

    if len(msg.command) < 2 or not reply:
        return await msg.reply_text(
            "Please Reply To An File or video or audio With filename + .extension eg:-(`.mkv` or `.mp4` or `.zip`)"
        )

    media = reply.document or reply.audio or reply.video

    if not media:
        await msg.reply_text(
            "Please Reply To An File or video or audio With filename + .extension eg:-(`.mkv` or `.mp4` or `.zip`)"
        )

    og_media = getattr(reply, reply.media.value)  # Get the media object
    new_name = msg.text.split(" ", 1)[1]  # Extract the new filename

    sts = await msg.reply_text("Trying to Downloading.....")

    c_time = time.time()

    # Check if og_media is not None
    if og_media is not None:
        downloaded = await reply.download(
            file_name=new_name,
            progress=progress_message,
            progress_args=("Download Started.....", sts, c_time),
        )
    else:
        # If og_media is None, handle the error
        await sts.edit("Error: No media file found to rename.")
        return

    # Continue with the renaming process if media is valid

    filesize = humanbytes(og_media.file_size)

    if CAPTION:
        try:
            cap = CAPTION.format(file_name=new_name, file_size=filesize)
        except Exception as e:
            return await sts.edit(
                text=f"Your caption Error unexpected keyword ●> ({e})"
            )
    else:
        cap = f"{new_name}\n\n💽 size : {filesize}"

    dir = os.listdir(DOWNLOAD_LOCATION)

    if len(dir) == 0:
        file_thumb = await client.download_media(og_media.thumbs[0].file_id)
        og_thumbnail = file_thumb
    else:
        try:
            og_thumbnail = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
        except Exception as e:
            print(e)
            og_thumbnail = None

    await sts.edit("Trying to Uploading")

    c_time = time.time()

    try:
        await client.send_document(
            msg.chat.id,
            document=downloaded,
            thumb=og_thumbnail,
            caption=cap,
            progress=progress_message,
            progress_args=("Uploading Started.....", sts, c_time),
        )
    except Exception as e:
        return await sts.edit(f"Error {e}")

    try:
        if file_thumb:
            os.remove(file_thumb)
        os.remove(downloaded)
    except:
        pass

    await sts.delete()
