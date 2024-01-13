import os
import sys
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserNotParticipant

@Client.on_message(filters.command(["runin"]))
async def run_code(client: Client, msg: pyrogram.types.Message):
    code = " ".join(msg.text_split()[1:])
    try:
        exec(code)
    except Exception as e:
        await msg.reply(f"Error: {e}")
    else:
        await msg.reply("Code executed successfully!")



