import pyrogram 
from pyrogram import Client, filters
import asyncio
from pyrogram.types import *

@Client.on_message(filters.command("start"))
async def start_session(client, message):
    
    await message.reply_text("Welcome to our bot...\n\nThis bot is intended to chat with people on Telegram")

@Client.on_message(filters.command("search"))
async def sart_session(client, message):
    
    v=await message.reply_text("searching partner...")
    await asyncio.sleep(5)
    z=await v.edit("Partner found")

@Client.on_message(filters.command("next"))
async def strt_session(client, message):
    
    a=await message.reply_text("searching partner...")
    await asyncio.sleep(5)
    b=await v.edit("Partner found")

@Client.on_message(filters.command("stop"))
async def stat_session(client, message):
    await message.reply_text("Stopped")

@Client.on_message(filters.text & ~filters.command("start","search","next","stop")
async def v_session(client, message):
   txt = message.text
   await client.send_message(
   
  
