from pyrogram import Client, filters 
import asyncio
from pyrogram.types import * 

OWNER_GID = -1004075001750

@Client.on_message(filters.command("send") & filters.private & filters.reply)
async def send(client, message:Message):
  if message.reply_to_message:
     user_id = message.from_user.id
     text = message.reply_to_message.text
     await message.reply_to_message.forward(OWNER_GID, message=text)
     await message.reply_text("message is sented, please wait for my admin to reply")
  else:
     await message.reply_text("reply to a message")
