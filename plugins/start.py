from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums, filters, Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT
import pyrogram

@Client.on_message(Filters.command("start"))
def start_command(client, message):
    keyboard = [[
        InlineKeyboardButton("Option 1", url="https://t.me/Unni0240"),
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message.reply_text("Welcome to my bot!", reply_markup=reply_markup)
