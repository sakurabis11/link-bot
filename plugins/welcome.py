import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from info import EVAL_ID, ADMINS

welcome_msg = []

@Client.on_message(filters.command("set_welcome") & filters.chat(int(EVAL_ID)))
async def set_welcome(client, message):
    user_id = message.from_user.id
    try:
        if user_id in ADMINS:
            welcome_msg = message.text.split()[1:]
            await message.reply_text(f"Set welcome message ✅\n\n{welcome_msg}")
        else:
            await message.reply_text(f"You are not an admin")
    except Exception as e: 
        await message.reply_text(f"Invalid command format. Usage: /set_welcome <message>\n\n{e}")

@Client.on_message(filters.command("see_welcome") & filters.chat(int(EVAL_ID)))
async def see_welcome(client, message):
  try:
    if welcome_msg and welcome_msg.strip():
      user_input = " ".join(welcome_msg)
      await client.send_message(message.chat.id, text=f"{user_input}")
    else:
      await message.reply_text("The welcome message is not set.")
  except Exception as e:
    await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command("delete_welcome") & filters.chat(int(EVAL_ID)))
async def delete_welcome(client, message):
    user_id = message.from_user.id
    try:
        if user_id in ADMINS:
            welcome_msg = None
            await message.reply_text("Welcome message deleted ✅")
        else:
            await message.reply_text(f"You are not an admin")
    except Exception as e:  
        await message.reply_text(f"An error occurred: {e}")
