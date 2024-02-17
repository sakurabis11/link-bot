from pyrogram import Client, filters, enums
from pyrogram.types import *

filters.command = bot.command
filters.group = group 
message.reply_text = message
client.send_message = send_msg 

@Client.on_message(bot.command("test"))
async def test(client, message):
    await message("hi {message.from_user.mention}")
