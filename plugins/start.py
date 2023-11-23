from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums, filters, Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT
import pyrogram

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    button = [[
        InlineKeyboardButton("Developer", url="https://t.me/MrTG_Coder")
    ],[
        InlineKeyboardButton("Support Group", url="https://t.me/+1YR5aYuCdr40N2M1"),
        InlineKeyboardButton("Support Channel", url="https://t.me/amal_nath_05"),
    ]]
    reply_markup = InlineKeyboardMarkup(button)

    await message.reply_text("**Welcome to my bot**", reply_markup=reply_markup)
