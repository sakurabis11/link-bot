from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums, filters, Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT
from Script import script

    ABOUT_TXT ="""<b>✯ Mʏ ɴᴀᴍᴇ: {}
✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a https://t.me/MrTG_Coder>ᴍʀ.ʙᴏᴛ ᴛɢ</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>
✯ Mʏ Sᴇʀᴠᴇʀ: <a href='https://www.render.com'>ʀᴇɴᴅᴇʀ </a>"""

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    button = [[
        InlineKeyboardButton("Developer", url="https://t.me/MrTG_Coder")
    ], [
        InlineKeyboardButton("Support Group", url="https://t.me/+1YR5aYuCdr40N2M1"),
        InlineKeyboardButton("Support Channel", url="https://t.me/amal_nath_05"),
    ]]
    reply_markup = InlineKeyboardMarkup(button)

    await message.reply_text("**Welcome to my bot**\n/help to get the help message\n/about just click this\n", reply_markup=reply_markup)

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    button = [[
        InlineKeyboardButton("Support Group", url="https://t.me/+1YR5aYuCdr40N2M1"),
        InlineKeyboardButton("Support Channel", url="https://t.me/amal_nath_05"),
    ]]
    reply_markup = InlineKeyboardMarkup(button)

    await message.reply_text("**HELP COMMANDS ARE:\n/openai {works in both group and private chat}\n**", reply_markup=reply_markup)

@Client.on_message(filters.command("about"))
async def about_command(client, message):
    await message.reply_text(ABOUT_TXT)

