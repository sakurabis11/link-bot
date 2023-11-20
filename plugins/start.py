import pyrogram
import asyncio
import pyrogram.errors.exceptions.bad_request_400 
from Script import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from info import API_ID, API_HASH, BOT_TOKEN, PORT

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(START_TXT)
