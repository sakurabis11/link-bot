from pyrogram import Client, filters
from pyrogram.types import *

@Client.on_message(filters.command("def"))
async def help_fn(client, message:Message):
 try:
   txt = message.text.split()[1::]
   txt = " ".join(txt)
   print(txt)
   x = help(txt)
   with open('help.txt', 'w+') as file:
       file.write(x)
   await client.send_document('help.txt', caption=f"{txt} help")
 except Exception as e:
   await message.reply_text(e)
