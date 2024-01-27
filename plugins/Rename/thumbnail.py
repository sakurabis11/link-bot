# CREDITS 🌟 - @Sunrises_24
from pyrogram import Client, filters 
from config import DOWNLOAD_LOCATION
import os

dir = os.listdir(DOWNLOAD_LOCATION)

@Client.on_message(filters.private & filters.command("set_thumb") & filters.reply)                            
async def set_tumb(bot, msg):
    if message.reply_to_message.photo:
      os.remove(f"{DOWNLOAD_LOCATION}/thumbnail.jpg")
      await bot.download_media(message=msg.photo.file_id, file_name=f"{DOWNLOAD_LOCATION}/thumbnail.jpg")               
      return await msg.reply(f"Your permanent thumbnail is saved ✅️")
      
    if not replied:
      return await update.reply_text("Ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ or ᴠɪᴅᴇᴏ.")
    if not ( replied.photo or replied.video ):
      return await update.reply_text("ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴀ ᴠᴀʟɪᴅ ᴍᴇᴅɪᴀ")

@Client.on_message(filters.private & filters.command("view"))                            
async def view_tumb(bot, msg):
    try:
        await msg.reply_photo(photo=f"{DOWNLOAD_LOCATION}/thumbnail.jpg", caption="this is your current thumbnail")
    except Exception as e:
        print(e)
        return await msg.reply_text(text="you don't have any thumbnail")

@Client.on_message(filters.private & filters.command(["del", "del_thumb"]))                            
async def del_tumb(bot, msg):
    try:
        os.remove(f"{DOWNLOAD_LOCATION}/thumbnail.jpg")
        await msg.reply_text("your thumbnail was removed❌")
    except Exception as e:
        print(e)
        return await msg.reply_text(text="you don't have any thumbnail‼️")


    
