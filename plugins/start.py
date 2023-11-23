from pyrogram import enums, filters, Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT
import pyrogram

@Client.on_message(filters.command("start"))
async def start_command(client, message):
      message.reply_text("Welcome to my bot!")
