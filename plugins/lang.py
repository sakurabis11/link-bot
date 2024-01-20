import pyrogram
from pyrogram import Client, filters

@Client.on_message(filters.command("kang") & filters.reply & filters.photo)
async def create_sticker(client, message):
    if message.reply_to_message.photo:
            try:
                photo = await message.reply_to_message.download()
                with open(photo, "rb") as sticker:
                    await message.reply_sticker(sticker) 
                    await message.reply_text("Photo converted to sticker and sent!")
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")
