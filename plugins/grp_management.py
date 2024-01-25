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
    await client.functions.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
    await message.reply_text("User has been kicked from this group")
  except PermissionError as e:
    await message.reply_text(str(e))
  except Exception as e:
    await message.reply_text(str(e))

@Client.on_message(filters.command("kickme"))
async def kick_i(client, message: Message):
  try:
     user_id = message.from_user.id
     await client.kick_chat_member(user_id)
     await message.reply_text(f"{message.user.mention} has been kicked from this group by himself/herself")
  except Exception as e:
     await message.reply_text(str(e))

@Client.on_message(filters.command("mute") & filters.group)
async def mute_user(client, message):
  try:
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
      raise PermissionError("You are not allowed to use this command")
    user_to_mute = message.reply_to_message.from_user
    await client.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(can_send_messages=False)
    )
    await message.reply_text("User muted successfully.")
  except Exception as e:
    await message.reply_text(str(e))

@Client.on_message(filters.command("unmute") & filters.group)
async def mute_user(client, message):
  try:
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
      raise PermissionError("You are not allowed to use this command")
    user_to_mute = message.reply_to_message.from_user
    await client.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(can_send_messages=True)
    )
    await message.reply_text("User unmuted successfully.")
  except Exception as e:
    await message.reply_text(str(e))
