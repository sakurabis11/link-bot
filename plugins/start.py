from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums, filters, Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT
from Script import script
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

ABOUT_TXT = """<b>✯ Mʏ ɴᴀᴍᴇ ɪS <^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </>
✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a href='https://t.me/MrTG_Coder'>ᴍʀ.ʙᴏᴛ ᴛɢ</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>
✯ Mʏ Sᴇʀᴠᴇʀ: <a href='https://www.render.com'>ʀᴇɴᴅᴇʀ </a>"""

@Client.on_message(filters.command("support"))
async def support_command(client, message):
    button = [
        [
            InlineKeyboardButton("Support Group", url="https://t.me/+1YR5aYuCdr40N2M1"),
            InlineKeyboardButton("Support Channel", url="https://t.me/amal_nath_05")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text("**These are my support group and channel. If any problem, send a report to the groups**", reply_markup=reply_markup)

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    button = [[
        InlineKeyboardButton("Help", callback_data="help"), 
        InlineKeyboardButton("About", callback_data="about")
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text("**Hi {first_name}, welcome to my bot! 🤖🎉\n**", reply_markup=reply_markup)

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    buttons = [[
         InlineKeyboardButton('Telegraph', callback_data='telegraph'),
         InlineKeyboardButton('Openai', callback_data='openai')
         ],[
         InlineKeyboardButton('Back', callback_data='start')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text("**HELPS**", reply_markup=reply_markup)

@Client.on_message(filters.command("about"))
async def about_command(client, message):
    button = [[
        InlineKeyboardButton("Back to Start", callback_data="start")
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text(ABOUT_TXT, reply_markup=reply_markup)

@Client.on_callback_query()
async def callback_handler(client, callback_query):
    query = callback_query

    if query.data == "start":
        buttons = [[
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("About", callback_data="about")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("**Hi {first_name}, welcome to my bot! 🤖🎉\n**", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    if query.data == "help":
        buttons = [[
            InlineKeyboardButton('Telegraph', callback_data='telegraph'),
            InlineKeyboardButton('Openai', callback_data='openai')
            ],[
            InlineKeyboardButton('Back', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("**HELPS**", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    if query.data == "telegraph"
        buttons = [[
            InlineKeyboardButton('Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("**/telegraph Rᴇᴘʟʏ Tᴏ A Pʜᴏᴛᴏ Oʀ Vɪᴅᴇᴏ**", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    if query.data == "openai"
        buttons = [[
            InlineKeyboardButton('Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("**/openai {ur question}\n Sometimes it will not work has very well**", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
    
    if query.data == "about":
        buttons = [[
            InlineKeyboardButton('Back', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(ABOUT_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

