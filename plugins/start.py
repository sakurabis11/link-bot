import pyrogram
import asyncio
import pyrogram.errors.exceptions.bad_request_400 
from Script import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from info import API_ID, API_HASH, BOT_TOKEN, PORT

# Define a function to handle the /start command
@Client.on_message(filters.command("start"))
def start_message(client, message):
    client.send_message("Hello! Welcome to my Telegram bot.")

