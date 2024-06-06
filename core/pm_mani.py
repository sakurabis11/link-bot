import pyrogram 
from pyrogram import Client, filters
import asyncio
from pyrogram.types import *
import os 
from os import environ

CHAT_TXT = int(os.environ.get("CHAT_TXT", "-1002207311121"))

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
   await client.send_message(CHAT_TXT, text=txt)

@Client.on_message(filter.command("r") & filters.chat(int(-1002207311121))
async def r_session(client, message):
   txt = message.text
   mrtg = message.text.split(" ", 2)
   user_id = int(mrtg[1])
   reply_text = mrtg[2]
   await client.send_message(user_id, text=reply_text)
   
  
