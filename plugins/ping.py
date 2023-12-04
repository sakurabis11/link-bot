import time
import logging
from pyrogram import filters, Client
from pyrogram.errors import FloodWait

PREFIX = '.'

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command("ping"["PREFIX"])
async def ping(client, message):
    try:
        start_time = time.time()
        await message.edit("🏓 Pong!")
        end_time = time.time()
        ping_time = float(end_time - start_time)
        await message.edit("🏓 Pong!\n⏱ Speed was : {0:.2f}s".format(round(ping_time, 2) % 60))
    except FloodWait as e:
        await message.edit("❗️ Flood wait! Please try again in {0:.2f} seconds.".format(e.x))
    except Exception as e:
        logging.error(e)
        await message.edit("❗️ An error occurred while processing your request.")

