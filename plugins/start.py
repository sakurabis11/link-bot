import pyrogram
import asyncio
import pyrogram.errors.exceptions.bad_request_400 
from Script import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from info import API_ID, API_HASH, BOT_TOKEN

@Client.on_callback_query(filters.command("start"))
async def start(query: CallbackQuery):
    buttons = [[
        InlineKeyboardButton("Hᴇʟᴩ 🕸️", callback_data="help"),
        InlineKeyboardButton("Aʙᴏᴜᴛ ✨", callback_data="about")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )
    await query.answer(MSG_ALRT)

@Client.on_callback_query(filters.regex(r"help"))
async def help(query: CallbackQuery):
    buttons = [[
        InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
        InlineKeyboardButton('🔒 ᴄʟᴏꜱᴇ', callback_data="close_data")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text="Pʀᴏᴄᴇꜱꜱɪɴɢ•"
    )
    await query.message.edit_text(
        text="Pʀᴏᴄᴇꜱꜱɪɴɢ••"
    )
    await query.message.edit_text(
        text="Pʀᴏᴄᴇꜱꜱɪɴɢ•••"
    )
    await query.message.edit_text(
        text=script.HELP_TXT.format(query.from_user.mention),
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex(r"about"))
async def about(query: CallbackQuery):
    buttons = [[
        InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
        InlineKeyboardButton('🔒 ᴄʟᴏsᴇ', callback_data='close_data')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=script.ABOUT_TXT.format(temp.B_NAME),
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )
