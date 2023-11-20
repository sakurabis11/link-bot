import pyrogram
import asyncio
import pyrogram.errors.exceptions.bad_request_400 
from Script import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from info import API_ID, API_HASH, BOT_TOKEN, PORT

@Client.on_message(filters.command("start"))
aysnc def start_command(client, message):
    # Welcome message
    welcome_message = "Welcome to my Telegram bot! 🎉"

    # Inline keyboard buttons
    keyboard = pyrogram.types.InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Support Group", url="https://t.me/amal_nath_05"),
                InlineKeyboardButton("Dᴇᴠᴇʟᴏᴩᴇʀ", url="https://t.me/MrTG_Coder"),
            ],
        ]
    )

    # Send the welcome message with the inline keyboard
    client.send_message(
        message.chat_id,
        text=welcome_message,
        reply_markup=keyboard,
    )
