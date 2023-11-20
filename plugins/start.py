import pyrogram
import asyncio
import pyrogram.errors.exceptions.bad_request_400 as bad_request
from Script import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.users_chats_db import db
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from info import API_ID, API_HASH, BOT_TOKEN, PORT, LOG_CHANNEL

# Define a function to handle the /start command
@Client.on_message(filters.command("start"))
async def start_message(client, message):
    await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)

    # Check if the chat exists in the database
    if not await db.get_chat(message.chat.id):
        # Get the number of chat members
        total = await client.get_chat_members_count(message.chat.id)

        # Send a log message to the LOG_CHANNEL
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))

        # Add the chat to the database
        await db.add_chat(message.chat.id, message.chat.title)
        return

    # Check if the user exists in the database
    if not await db.is_user_exist(message.from_user.id):
        # Add the user to the database
        await db.add_user(message.from_user.id, message.from_user.first_name)

        # Send a log message to the LOG_CHANNEL
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('bot.log')
    except Exception as e:
        await message.reply(str(e))
