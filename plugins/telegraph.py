import os, asyncio
import aiohttp
from pyrogram import Client, filters
from telegraph import upload_file
from utils import get_file_id
import shutil

TG_DOWNLOAD_DIRECTORY = "./DOWNLOADS/"

@Client.on_message(
  filters.command("telegraph")
)
async def telegraph(client, message):
  replied = message.reply_to_message

  if not replied:
    await message.reply_text("Reply to a supported media file")
    return

  file_path = get_file_path(replied)

  if not file_path:
    await message.reply_text("Not supported!")
    return

  try:
    response = upload_file(file_path)
  except Exception as document:
    await message.reply_text(message, text=document)
  else:
    await message.reply(
      f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>",
      disable_web_page_preview=True
    )

  # Only delete the file if the upload was successful
  if os.path.exists(file_path) and response:
    os.remove(file_path)

def get_file_path(message):
  if message.photo or message.video:
    file_path = message.download(TG_DOWNLOAD_DIRECTORY)
  elif message.document:
    file_path = message.document.file_path
  else:
    return None

  return file_path
