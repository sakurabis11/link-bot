import pyrogram 
from pyrogram import Client, filters
from pyrogram.types import Message
from info import EVAL_ID, ADMINS

welcome_msg = []

@Client.on_message(filters.command("set_welcome") & filters.user(EVAL_ID))
async def setw_elcome(client, message):
 user_id = message.from_user.id
 if user_id in ADMINS:
   welcome_msg = message.text.split()[1:]
   await message.reply_text("set welcome message ✅")
 else:
   await message.reply_text(f"You are not admin")

@Client.on_message(filters.command("see_welcome"))
async def seew_elcome(client, message):
  if welcome_msg is None:
    await message.reply_text("The welcome message is none")
  else:
    await message.reply_text(welcome_msg)

@Client.on_message(filters.command("delete_welcome") & filters.user(EVAL_ID))
async def setw_elcome(client, message):
 user_id = message.from_user.id
 if user_id in ADMINS:
   if welcome_msg is None:
     await message.reply_text("welcome message is None")
   else:
     welcome_msg = None
     await message.reply_text("delete welcome message ✅")
 else:
   await message.reply_text(f"You are not admin")
