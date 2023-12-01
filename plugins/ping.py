import time
from pyrogram import Client, filters
from info import ADMINS

prefix = '.'

@Client.on_message(filters.command("ping", [prefix=='.']) & filters.user(ADMINS))
async def ping(client, message):
  start_time = time.time()
  reply_message = await message.reply_text("...")
  end_time = time.time()
  time_taken_milliseconds = (end_time - start_time) / 1000
  await reply_message.edit(f"Pong!\n{time_taken_milliseconds:.3f} ms")
