from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums, filters, Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT
import pyrogram

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    button = [[
        InlineKeyboardButton("Developer", url="https://t.me/Unni0240"),
    ]]
    reply_markup = InlineKeyboardMarkup(button)

    await message.reply_text("**Welcome to my bot**", reply_markup=reply_markup)
