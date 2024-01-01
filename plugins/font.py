from pyrogram import Client, filters
from pyrogram.types import *
from plugins.sd_bots.font_list import Font


@Client.on_message(filters.command("font"))
async def font_handler(client, message):
    text = message.text.split(" ", 1)[1]

    keyboard = [[
            InlineKeyboardButton("SD", callback_data="sd")
        ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("sd font", reply_markup=reply_markup)

@Client.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    font_class = Font()

    if data == "sd":
        stylized_text = font_class.SD(text)
    
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(text=f"{stylized_text}", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
