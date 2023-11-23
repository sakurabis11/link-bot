from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums, filters, Client
from Script import script
from info import API_ID, API_HASH, BOT_TOKEN, PORT
import asyncio
import re

MSG_ALRT = "HI"

@Client.on_messsage(filter.command("start"))
async def start_command(client, message):
    buttons = [[
        InlineKeyboardButton("Developer ♾️", url='https://t.me/Unni0240')
    ]]
    message_text = "Hello"
    reply_markup = InlineKeyboardMarkup(buttons)
    
