from pyrogram import Client, filters 
import asyncio
from pyrogram.types import * 

OWNER_GID = -1004075001750

@Client.on_message(filters.command("send") & filters.private)
async def send(client, message:Message):
  msg = message.text.split()[1:]
  if len(msg) == 1:
    return await message.reply("**usage:**\n<code>/send (message)</code>")
  msg = " ".join(msg)
  await client.forward_messages(chat_id=OWNER_GID, messages=msg)
  await message.reply("**message sent**")

@Client.on_message(filters.command("reply") & filters.chat(int(OWNER_GID)) & filters.reply)
async def reply(client, message:Message):
  rply = message.text.split()[1:]
  user = message.reply_to_message.forward_from.id
  if len(rply) == 1:
    return await message.reply("**usage:**\n<code>/reply (message)</code>")
  if not message.reply_to_message:
    return await message.reply("**reply to forward message")
  rply = " ".join(msg)
  await client.send_message(user, rply)
  
  
