import pyrogram 
from pyrogram import filters, Client
from pyrogram.types import Message
import psutil
import time
import os
from info import EVAL_ID

def format_uptime(seconds):
    days = seconds // (24*60*60)
    seconds %= (24*60*60)
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    return f"{days} days, {hours} hours, {minutes} minutes"

@Client.on_message((filters.text) & filters.chat(int(EVAL_ID)))
async def msg(client, message: Message):
    if message.text == "hi":
        await message.reply_text(f"Hello {message.from_user.mention}")
    elif message.text == "hello":
        await message.reply_text(f"Hello {message.from_user.mention}")
    elif message.text == ".alive":
        uptime = format_uptime(time.time() - psutil.boot_time())
        await message.reply_text(f"I am alive\n\nI am running on {uptime}")
    else:
        pass
