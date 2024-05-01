import pyrogram
from pyrogram import Client , filters , enums
from pyrogram.types import BotCommand
import requests as re
import os
import asyncio
import sys
import uvloop
from os import environ
from utils import restart_all_bots
import pymongo
from pymongo import MongoClient
from info import API_ID , API_HASH , LOG_CHANNEL , DATABASE_URI , DATABASE_NAME , ADMINS, LOG_CHANNEL_INFORM, LOG_CHANNEL_ERROR
from dotenv import load_dotenv

LOG_clone_CHANNEL = int(environ.get('LOG_clone_CHANNEL' , '-1002100856982'))

load_dotenv()

client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["clone_bots"]


@Client.on_message(filters.command('clone') & filters.private)
async def clone_handler(client , message):
    await message.reply_text(
        "Gᴏ ᴛᴏ @BotFather ᴀɴᴅ ᴄʀᴇᴀᴛᴇ ᴀ ɴᴇᴡ ʙᴏᴛ.\n\nsᴇɴᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴡɪᴛʜ ᴄᴏᴍᴍᴀɴᴅ /add .(ᴇɢ:- /add 𝟷𝟸𝟹𝟺𝟻𝟼:ᴊʙᴅᴋʜsʜᴅᴠᴄʜᴊʜᴅʙʜs-sʜʙ)")


@Client.on_message(filters.command('add') & filters.private)
async def add_handler(client , message):
    try:
        new_message = message.text.split()[1:]
        bot_token = " ".join(new_message)
        existing_token = collection.find_one({"bot_token": bot_token})
        if existing_token is None:
            pass
        else:
            await client.send_message(LOG_clone_CHANNEL , text=existing_token)
        if existing_token:
            await message.reply_text("Tʜɪs ʙᴏᴛ ᴛᴏᴋᴇɴ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ.")
            return
        a = await message.reply_text("ᴄʟᴏɴɪɴɢ sᴛᴀʀᴛᴇᴅ")
        c_bot = Client(
            name="clone" ,
            api_id=API_ID ,
            api_hash=API_HASH ,
            bot_token=bot_token ,
            plugins={"root": "c_plugins"}
        )
        try:
            await c_bot.start()
            mine = await c_bot.get_me()
            await c_bot.set_bot_commands(
                [BotCommand("start" , "to check the bot alive or not.") ,
                 BotCommand("help" , "to get the help buttons.") ,
                 BotCommand("about" , "to get the bot details.") ,
                 BotCommand("ai" , "ask your doubt to gemini.") ,
                 BotCommand("song" , "to get the song.") ,
                 BotCommand("convert" , "convert video to audio.")]
            )
            await a.edit(f"**@{mine.username} ʜᴀs sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ**")
            await client.send_message(LOG_CHANNEL_INFORM, text=f"#new_bot\n\n@{mine.username} ʜᴀs ʙᴇᴇɴ ᴄʟᴏɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
        except Exception as e:
            await message.reply_text(f'Error - <code>{e}</code>')
            return

        bot_info = {
            "bot_token": bot_token ,
            "user_id": message.from_user.id ,
            "user_fname": message.from_user.first_name ,
            "username": mine.username
        }
        if bot_info:
            collection.insert_one(bot_info)
            await client.send_message(LOG_clone_CHANNEL , text=bot_info)
        else:
            await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴄʟᴏɴᴇ ʙᴏᴛ. Iɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴏʀ ᴇʀʀᴏʀ ʀᴇᴛʀɪᴇᴠɪɴɢ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.")
    except Exception as e:
        await message.reply_text(e)


@Client.on_message(filters.command('my_bots') & filters.private)
async def list_cloned_bots(client , message):
    try:
        user_id = message.from_user.id
        bot_infos = collection.find({"user_id": user_id})
        response = "**Yᴏᴜʀ Cʟᴏɴᴇᴅ Bᴏᴛs:**\n"

        if not bot_infos:
            await message.reply_text("Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴄʟᴏɴᴇᴅ ᴀɴʏ ʙᴏᴛs ʏᴇᴛ.")
            return

        for bot_info in bot_infos:
            username = bot_info.get("username" , "N/A")
            response += f"- @{username}\n"

        await message.reply_text(response)

    except Exception as e:
        await message.reply_text(f"An error occurred:\n<code>{e}</code>")


@Client.on_message(filters.command('delete') & filters.private)
async def delete_bot_handler(client, message):
    try:
        bot_username = message.text.split()[1]

        if not bot_username.startswith("@"):
            await message.reply_text("Invalid bot username format. Use '@username'.")
            return

        bot_info = collection.find_one_and_delete({
          "username": bot_username.strip("@") ,
          "user_id": message.from_user.id
        })

        if not bot_info:
            await message.reply_text("Couldn't find a bot with that username belonging to you.")
            return
        try:
            collection.delete_one(bot_info)
            await message.reply_text(f"{bot_username} ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʟɪsᴛ.\n\nɪᴛ ᴡɪʟʟ ᴛᴀᴋᴇ sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛʜᴀᴛ ʙᴏᴛ")
            await client.send_message(LOG_CHANNEL_INFORM, text=f"#delete_bot\n\n{bot_username} ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ.")
        except Exception as e:
            await message.reply_text(f"Error stopping/deleting the bot:\n<code>{e}</code>")

    except Exception as e:
        await message.reply_text(f"An error occurred:\n<code>{e}</code>")


@Client.on_message(filters.command('see_bots') & filters.user(ADMINS))
async def list_bots_handler(client , message):
    try:
        u_id = message.from_user.id
        if u_id in ADMINS:
            number_of_cloned_bots = collection.count_documents({})
            print(number_of_cloned_bots)
            bot_infos = collection.find({})
            response = "**Cloned Bots:**\n"

            if not bot_infos:
                await message.reply_text("No cloned bots found.")
                return

            for bot_info in bot_infos:
                username = bot_info.get("username" , "N/A")
                user_id = bot_info.get("user_id" , "N/A")
                user_finame = bot_info.get("user_fname" , "N/A")
                response += f"- Username: @{username}\n- User ID: {user_id}\n- Name: <a href='tg://user?id={user_id}'><b>{user_finame}</b></a>\n\n"

            await message.reply_text(f"ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇ ʙᴏᴛs: {number_of_cloned_bots}\n\n{response}")
        else:
            await message.reply_text("This command is only accessible in the admin chat.")
    except Exception as e:
        await message.reply_text(f"An error occurred:\n<code>{e}</code>")
