from pyrogram import Client, filters
from pyrogram.types import *

@Client.on_message(filters.command("def"))
async def help_fn(client, message:Message):
   txt = message.text.split()[1::]
   await message.reply_text(help(txt))
