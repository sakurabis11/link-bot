from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import os
import psutil
import time
from os import environ

EVAL_ID = int(os.environ.get("EVAL_ID", "-1002002636126"))

def format_uptime(seconds):
    days = seconds // (24*60*60)
    seconds %= (24*60*60)
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    return f"{days} days, {hours} hours, {minutes} minutes"

@Client.on_message(filters.text & filters.chat(int(EVAL_ID)))
async def echo(client: Client, message: Message):
    try:
        msg = message.text
        msg = msg.lower()
        if msg == "hi":
            await message.reply_text(f"Hello {message.from_user.mention}")
        elif msg in "hii":
            await message.reply_text(f"Hello {message.from_user.mention}")
        elif msg == "hello":
            await message.reply_text(f"hi {message.from_user.mention}")  
        elif msg == "helo":
            await message.reply_text(f"hi {message.from_user.mention}")  
        elif msg == "bye":
            await message.reply_text(f"Bye {message.from_user.mention}")
        elif msg == "how are you":
            await message.reply_text("I am just a telegram bot, i donot have any feelings. how are you?")
        elif msg == "how are you bot?":
            await message.reply_text("I am just a telegram bot, i donot have any feelings. how are you?")
        elif msg == "how are you ?":
            await message.reply_text("I am just a telegram bot, i donot have any feelings. how are you?")
        elif msg == "how are you bot ?":
            await message.reply_text("I am just a telegram bot, i donot have any feelings. how are you?")
        elif msg == "how are you?":
            await message.reply_text("I am just a telegram bot, i donot have any feelings. how are you?")
        elif msg == "how are you bot":
            await message.reply_text("I am just a telegram bot, i donot have any feelings. how are you?")
        elif msg == "i am fine":
            await message.reply_text("Do u use my features")
        elif msg == "yes":
            await message.reply_text("Thanks for using my feature")
        elif msg == "no":
            await message.reply_text("use it click /help")
        elif msg == "ok i will try":
            await message.reply_text("mm")
        elif msg == "who is your owner ?":
            await message.reply_text("@MrTG_Coder")
        elif msg == "who is ur owner ?":
            await message.reply_text("@MrTG_Coder") 
        elif msg == "who is your owner?":
            await message.reply_text("@MrTG_Coder")
        elif msg == "who is ur owner?":
            await message.reply_text("@MrTG_Coder") 
        elif msg == "which model are you using ?":
            await message.reply_text("<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </> is made me, i think you should ask him.")
        elif msg == "which model are you using?":
            await message.reply_text("<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </> is made me, i think you should ask him.")
        elif msg == "which ai are you using ?":
            await message.reply_text("<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </> is made me, i think you should ask him.")
        elif msg == "which ai are you using?":
            await message.reply_text("<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </> is made me, i think you should ask him.")    
        elif msg == "which ai model are you using ?":
            await message.reply_text("<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </> is made me, i think you should ask him.")
        elif msg == "which ai model are you using?":
            await message.reply_text("<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </> is made me, i think you should ask him.") 
        elif msg == "what is your name ?":
            await message.reply_text("my name is ᴏʙᴀɴᴀɪ")
        elif msg == "what is your name?":
            await message.reply_text("my name is ᴏʙᴀɴᴀɪ")
        elif msg == "what is ur name ?":
            await message.reply_text("my name is ᴏʙᴀɴᴀɪ")
        elif msg == "what is ur name?":
            await message.reply_text("my name is ᴏʙᴀɴᴀɪ")
        elif msg == "how to deploy a telegram bot":
            await message.reply_text("ask him: @MrTG_Coder")
        elif msg == "how to deploy a bot?":
            await message.reply_text("ask him: @MrTG_Coder")
        elif msg == "how to deploy a telegram bot ?":
            await message.reply_text("ask him: @MrTG_Coder")
        elif msg == "how to deploy a telegram bot?":
            await message.reply_text("ask him: @MrTG_Coder")

        elif msg == "how to deploy a bot":
            await message.reply_text("ask him: @MrTG_Coder")
        elif msg == "how to deploy a bot?":
            await message.reply_text("ask him: @MrTG_Coder")
        elif msg == "how to deploy a bot ?":
            await message.reply_text("ask him: @MrTG_Coder")
        elif msg == "how to deploy a bot?":
            await message.reply_text("ask him: @MrTG_Coder")

        elif msg == "can u send ur repo":
            await message.reply_text("yup, why not repo:- https://github.com/MrTG-CodeBot/Obanai")
        elif msg == "which server are u using ?":
            await message.reply_text("idk")
        elif msg == "which server are u using?":
            await message.reply_text("idk")     
        elif msg == "which server are u using":
            await message.reply_text("idk")  
        elif msg == "are you advance chatbot?":
            await message.reply_text("nope")
        elif msg == "are you advance chatbot ?":
            await message.reply_text("nope")
        elif msg == "are you advance chatbot":
            await message.reply_text("nope")
        elif msg == "":
            await message.reply_text("nope")
        elif msg == "are you advance chatbot":
            await message.reply_text("nope")

        elif msg == "can u send the uptime of urs":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can you send the uptime of your's":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can u send the uptime of ur's":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can u send the uptime of urs?":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 

        elif msg == "can u send the uptime of urs?":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can you send the uptime of your's?":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can u send the uptime of ur's?":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can u send the uptime of urs ?":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>")

        elif msg == "can u send the uptime of urs ?":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can you send the uptime of your's ?":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can u send the uptime of ur's ?":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>") 
        elif msg == "can u send the uptime of urs":
            uptime = format_uptime(time.time() - psutil.boot_time())
            await message.reply_text(f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>")
        elif msg == "it is not for ur's":
            await message.reply_text(f"ok {message.from_user.mention}")
        elif msg == "it is not for urs":
            await message.reply_text(f"ok {message.from_user.mention}")
        elif msg == "it is not for yours":
            await message.reply_text(f"ok {message.from_user.mention}")
        elif msg == "it is not for your's":
            await message.reply_text(f"ok {message.from_user.mention}")           
        else:
            await message.reply_text(f"{message.from_user.mention} i didn't understand or i am not advanced bot.")
    except Exception as e:
        await message.reply_text(f"{e}")
