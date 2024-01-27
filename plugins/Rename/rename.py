import time
import os
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncio import sleep
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from info import *  # Consider providing details of this file's contents
from plugins.Rename.r_utils import progress_message, humanbytes

DOWNLOAD_LOCATION = "./DOWNLOADS"

@Client.on_message(filters.private & filters.command("rename"))
async def rename_file(bot, msg):
    reply = msg.reply_to_message
    if len(msg.command) < 2 or not reply:
        return await msg.reply_text("Please Reply To An File or video or audio With filename + .extension eg:-(`.mkv` or `.mp4` or `.zip`)")

    media = reply.document or reply.audio or reply.video
    if not media:
        await msg.reply_text("Please Reply To An File or video or audio With filename + .extension eg:-(`.mkv` or `.mp4` or `.zip`)")

    og_media = getattr(reply, reply.media.value)
    new_name = msg.text.split(" ", 1)[1]

    sts = await msg.reply_text("Trying to Downloading.....⚡")
    c_time = time.time()
    downloaded = await reply.download(file_name=new_name, progress=progress_message, progress_args=("Download Started...⚡️", sts, c_time))
    filesize = humanbytes(og_media.file_size)

    c_caption = await db.get_caption(update.message.chat.id)  
    c_thumb = await db.get_thumbnail(update.message.chat)

    if c_caption:
        try:
            caption = c_caption.format(file_name=new_name, file_size=filesize) 
        except Exception as e:
            return await sts.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
        caption = f"**{new_filename}**"

    dir = os.listdir(DOWNLOAD_LOCATION)
    if len(dir) == 0:
        c_thumb = await bot.download_media(og_media.thumbs[0].file_id)
        og_thumbnail = c_thumb
    else:
        try:
            og_thumbnail = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
        except Exception as e:
            print(e)        
            og_thumbnail = None
        
    await sts.edit("Trying to Uploading...⚡")
    c_time = time.time()
    try:
        await bot.send_document(msg.chat.id, document=downloaded, thumb=og_thumbnail, caption=cap, progress=progress_message, progress_args=("Uploade Started.....", sts, c_time))        
    except Exception as e:  
        return await sts.edit(f"Error {e}")                       
    try:
        if file_thumb:
            os.remove(file_thumb)
        os.remove(downloaded)      
    except:
        pass
    await sts.delete()

    await sts.delete()
