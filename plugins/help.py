from pyrogram import enums, filters, Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT

@Client.on_message(filters.command("help"))
async def help_command(client, message):
      message.reply_text("Welcome to my bot!")
