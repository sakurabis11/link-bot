from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS

# Replace with your bot's API token
CHANNEL_ID = -1001717634274 
CAPTION = "@mrtgcoderbot"

auto_caption_enabled = False

@Client.on_message(filters.command(["auto_caption"]))
async def handle_auto_caption(client, message):
    global auto_caption_enabled
    if message.from_user.id == ADMINS:
        status = message.command[1].lower()
        if status == "on":
            auto_caption_enabled = True
            await message.reply("Auto caption enabled")
        elif status == "off":
            auto_caption_enabled = False
            await message.reply("Auto caption disabled")
        else:
            await message.reply("Invalid command. Use /auto_caption on or /auto_caption off")

@Client.on_message(filters.document & filters.chat(CHANNEL_ID))
async def handle_document(client, message):
    global auto_caption_enabled
    if auto_caption_enabled:
        file_name = message.document.file_name
        file_size = f"{message.document.file_size} bytes"
        new_caption = f"{file_name}\n{file_size}\nCAPTION"
        await message.edit_caption(new_caption)

