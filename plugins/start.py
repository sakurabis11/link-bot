from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums, filters, Client
from Script import script
from info import API_ID, API_HASH, BOT_TOKEN, PORT
import asyncio
import re

MSG_ALRT = "HI"

async def handle_callback_query(query):
    if query.data == "start":
        await show_start_menu(query)
    elif query.data == "help":
        await show_help_menu(query)
    elif query.data == "about":
        await show_about_menu(query)

async def show_start_menu(query):
    buttons = [
        [
            InlineKeyboardButton("Hᴇʟᴩ 🕸️", callback_data="help"),
            InlineKeyboardButton("Aʙᴏᴜᴛ ✨", callback_data="about")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    message_text = script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME)

    await edit_message_with_processing(query.message, message_text, reply_markup)

async def show_help_menu(query):
    buttons = [
        [
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔒 ᴄʟᴏꜱᴇ', callback_data="close_data")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    processing_messages = ["Pʀᴏᴄᴇꜱꜱɪɴɢ•", "Pʀᴏᴄᴇꜱꜱɪɴɢ••", "Pʀᴏᴄᴇꜱꜱɪɴɢ•••"]
    for text in processing_messages:
        await query.message.edit_text(text=text)
    
    help_text = script.HELP_TXT.format(query.from_user.mention)
    await edit_message_with_processing(query.message, help_text, reply_markup)

async def show_about_menu(query):
    buttons = [
        [
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close_data')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    about_text = script.ABOUT_TXT.format(temp.B_NAME)
    await edit_message_with_processing(query.message, about_text, reply_markup)

async def edit_message_with_processing(message, text, reply_markup):
    await message.edit_text(text="Pʀᴏᴄᴇꜱꜱɪɴɢ•")
    await message.edit_text(text="Pʀᴏᴄᴇꜱꜱɪɴɢ••")
    await message.edit_text(text="Pʀᴏᴄᴇꜱꜱɪɴɢ•••")
    await message.edit_text(text=text, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
