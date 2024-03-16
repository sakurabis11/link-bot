# I am mrtgcoder, i am presenting a chat bot using if- else statement

import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS
from database.users_db import db
from Script import script

import os
import psutil
import time

def format_uptime(seconds):
    days = seconds // (24*60*60)
    seconds %= (24*60*60)
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    return f"{days} days, {hours} hours, {minutes} minutes"

@Client.on_message(filters.command("tell") & filters.private & filters.user(ADMINS))
async def echo(client, message: Message):
 try:
     msg = message.text.split()[1::]
     msg = " ".join(msg)
     msg = msg.replace("/"," ").replace("."," ").replace(",", " ").replace("''"," ").replace("'"," ").replace("[]"," ").replace("{}"," ").replace("()"," ").replace("`"," ").replace("~"," ").replace("!"," ").replace("@"," ").replace("#"," ").replace("$"," ").replace("%"," ").replace("^"," ").replace("&"," ").replace("*"," ").replace("("," ").replace(")"," ").replace("{"," ").replace("}"," ").replace("["," ").replace("]"," ").replace("-"," ").replace("_"," ").replace("+"," ").replace("="," ")
     msg = msg.lower()
     if not msg:
       await message.reply_text("provide a input")
       return

     if ("hi" or "hii" or "hiii" or "hello" or "hellu" or "helo") in msg:
       await message.reply_text(f"Hello {message.from_user.mention}")
     elif ("good morning" or "morning") in msg:
       await message.reply_text(f"good morning {message.from_user.mention}")
     elif ("good evening" or "evening") in msg:
       await message.reply_text(f"good morning {message.from_user.mention}")
     elif ("how are you" or "how are u") in msg:
       await message.reply_text("I am just a telegram bot, i don't have any feelings. How are you?")    
     elif ("i am fine" or "fine") in msg:
       await message.reply_text("Oh great\n\nDo u use my features?")
     elif ("yes" or "yup" or "i used the features") in msg:
       await message.reply_text("Ch nice, thank u for using me.")
     elif ("no" or "nope" or "nop") in msg:
       await message.reply_text("Click /help to use my features.")  
     elif ("who is your owner" or "owner name") in msg:
       await message.reply_text("@MrTG_Coder, He is the owner.")
     elif ("which model are you using" or "which ai model are you using" or "which ai is used for chatbot") in msg:
       await message.reply_text("<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </> is made me, i think you should ask him.")
     elif ("what is your name" or "ur name" or "your name") in msg:
       await message.reply_text("My name is ᴏʙᴀɴᴀɪ")  
     elif ("how to deploy a telegram bot" or "how to deploy a bot" ) in msg:
       await message.reply_text("Ask him: @MrTG_Coder")
     elif ("can u send ur repo" or "can you send your repo") in msg:
       await message.reply_text("yup, why not repo:- https://github.com/MrTG-CodeBot/Obanai", disable_web_page_preview=True)
     elif ("which server are you using" or "which platform is you were deployed") in msg:
       await message.reply_text("Idk")  
     elif ("are you advance chatbot" or "you are a advance chatbot") in msg:
       await message.reply_text("Nope, i upgrading all day by day")
     elif ("can u send the uptime of urs" or "can u send the uptime of yours") in msg:
       uptime = format_uptime(time.time() - psutil.boot_time())
       await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>")
     elif ("can you generate images" or "do you generate images by text") in msg:
       await message.reply_text("Nope")  
     elif ("how many users are using this bot" or "how many users do you have" or "group") in msg:
       users = await db.total_users_count()
       chats = await db.total_chat_count()
       await message.reply_text(text=script.STATUS_TXT.format(users, chats))
     else:
       pass
 except Exceptions as e:
       await message.reply_text(f"{e}")
