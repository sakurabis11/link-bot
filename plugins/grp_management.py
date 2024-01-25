from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import *

@Client.on_message(filters.command("kick"))
async def kick_user(client, message: Message):
  try:
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
      raise PermissionError("You are not allowed to use this command")

    user_id = message.reply_to_message.from_user.id
    await client.kick_chat_member(message.chat.id, user_id)
    await message.reply_text("User has been kicked from this group")
  except PermissionError as e:
    await message.reply_text(str(e))
  except Exception as e:
    await message.reply_text(str(e))

@Client.on_message(filters.command("kickme"))
async def kick_i(client, message: Message):
  try:
     user_id = message.from_user.id
     await client.kick_chat_member(message.chat.id, user_id)
     await message.reply_text(f"{message.user.mention} has been kicked from this group by himself/herself")
  except Exception as e:
     await message.reply_text(str(e))