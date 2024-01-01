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

    await callback_query.message.reply_text(stylized_text)
    await callback_query.answer()

