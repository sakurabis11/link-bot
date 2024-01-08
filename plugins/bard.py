import os

from pyrogram import Client, filters
import google.generativeai as GenerativeAI

bard = GenerativeAI()

@aClient.on_message(filters.command("bard"))
async def handle_bard(client, message):
    query = message.text.split(" ", 1)[1]  

    try:
       
        response = bard.create_text(query)
        await message.reply_text(response.text)  
    except Exception as e:
  
        await message.reply_text(f"Error: {e}")


