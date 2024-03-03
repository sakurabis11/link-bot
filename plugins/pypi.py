import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pypi_search import *

@Client.on_message(filters.command("pypi"))
async def pypi_search(client: Client, message: Message):
 try:
    query = message.text.split(" ", maxsplit=1)[1]
    try:
        result = search(query)
        response = f"**{result['info']['name']}**\n\n"
        response += f"**Version:** {result['info']['version']}\n"

    except Exception as e:
        response = f"Error 1: {str(e)}"
    await message.reply(response)
 except Exception as e:
    await message.reply_text(f"Error 2:{str(e)}")


