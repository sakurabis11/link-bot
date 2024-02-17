from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from info import ADMINS

lock_types=[]

@Client.on_message(filters.command("lock") & filters.group & filters.user(ADMINS)
async def lock(client, message: Message):
    lock=message.split(" ", 1)
    lock_types=lock
    await message.reply_text(f"{lock_types} is added succesfully")

@Client.on_message()
async def chheck(client, message: Message):
    if message.text == lock_types:
      message.delete()
      k=await message.reply_text(f"{message.from_user.mention} you are using blacklist word, so we delete that message")
      asyncio(10)
      k.delete()
    return
