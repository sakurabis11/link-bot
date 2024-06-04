import pyrogram 
from pyrogram import Client, filters
from info import ADMINS

@Client.on_message(filters.txt | filters.photo & filters.private & ~filters.user(ADMINS))
async def start_non(client, message):
  await message.reply_text("Sorry the bot is under maintenance work")
  
