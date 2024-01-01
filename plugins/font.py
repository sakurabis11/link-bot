from pyrogram import Client, filters
from plugins.sd_bots.font_list import Font

@Client.on_message(filters.command("font"))
async def stylize_text(client, message):
    text_to_stylize = message.text.split(" ", 1)[1]  
    stylized_text = Font.SD(text_to_stylize)  

    await message.reply_text(stylized_text)  
