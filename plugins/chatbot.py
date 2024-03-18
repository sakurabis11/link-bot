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
     msg = msg.replace(" ","_")

     if ("hi" or "hii" or "hiii" or "hello" or "hellu" or "helo") in msg:
       await message.reply_text(f"Hello {message.from_user.mention}")
     elif ("good_morning" or "morning" or "mrng") in msg:
       await message.reply_text(f"good morning {message.from_user.mention}")
     elif ("good_evening" or "evening" or "evning") in msg:
       await message.reply_text(f"good morning {message.from_user.mention}")
     elif ("how_are_you" or "how_are_u" or "how_are_you_today") in msg:
       await message.reply_text("I am just a telegram bot, i don't have any feelings. How are you?")    
     elif ("i_am_fine" or "fine" or "good_day") in msg:
       await message.reply_text("Oh great\n\nDo u use my features?")
     elif ("yes" or "yup" or "i_used_the_features") in msg:
       await message.reply_text("Ch nice, thank u for using me.")
     elif ("no" or "nope" or "nop") in msg:
       await message.reply_text("Click /help to use my features.")  
     elif ("who_is_your_owner" or "owner_name") in msg:
       await message.reply_text("@MrTG_Coder, He is the owner.")
     elif ("which_model_are_you_using" or "which_ai_model_are_you_using" or "which_ai_is_used_for_chatbot") in msg:
       await message.reply_text("<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </> is made me, i think you should ask him.")
     elif ("what_is_your_name" or "ur_name" or "your_name") in msg:
       await message.reply_text("My name is ᴏʙᴀɴᴀɪ")  
     elif ("how_to_deploy_a_telegram_bot" or "how_to_deploy_a_bot" ) in msg:
       await message.reply_text("Ask him: @MrTG_Coder")
     elif ("can_u_send_ur_repo" or "can_you_send_your_repo") in msg:
       await message.reply_text("yup, why not repo:- https://github.com/MrTG-CodeBot/Obanai", disable_web_page_preview=True)
     elif ("which_server_are_you_using" or "which_platform_is_you_were_deployed") in msg:
       await message.reply_text("Idk")  
     elif ("are_you_advance_chatbot" or "you_are_a_advance_chatbot") in msg:
       await message.reply_text("Nope, i upgrading all day by day")
     elif ("can_u_send_the_uptime_of_urs" or "can_u_send_the_uptime_of_yours") in msg:
       uptime = format_uptime(time.time() - psutil.boot_time())
       await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>")
     elif ("can_you_generate_images" or "do_you_generate_images_by_text") in msg:
       await message.reply_text("Nope")  
     elif ("how_many_users_are_using_this_bot" or "how_many_users_do_you_have" or "group") in msg:
       users = await db.total_users_count()
       chats = await db.total_chat_count()
       await message.reply_text(text=script.STATUS_TXT.format(users, chats))
     else:
       pass
 except (Exception1, Exception2) as e:
       await message.reply_text(f"{e}")
