from pyrogram import Client, filters, enums
from pyrogram.types import *

@Client.on_message = @bot.message
filters.command = bot.command
filters.group = group 
message.reply_text = message
client.send_message = send_msg 
