import pyrogram
from pyrogram import Client, filters, enums
import pymongo
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pymongo import MongoClient
import os
from Script import script
from info import DATABASE_URI_2, DATABASE_NAME_2
from database_pic.pic_users_db import sd
from os import environ

ABOUT_TXT="""
✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a href='https://t.me/MrTG_Coder'>ᴍʀ.ʙᴏᴛ ᴛɢ</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>
✯ Mʏ Sᴇʀᴠᴇʀ: <a href='https://t.me/mrtgcoderbot'>ᴏʙᴀɴᴀɪ</a>
✯ Pʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: ᴠ2.0.106
✯ Mʏ ᴠᴇʀsɪᴏɴ: ᴠ2.0
"""

client = MongoClient(DATABASE_URI_2)
db = client[DATABASE_NAME_2]
collection = db["pic_db"]

PIC_LOG_CHANNEL = os.environ.get('PIC_LOG_CHANNEL', '-1002144220682')

@Client.on_message(filters.command("start"))
async def start(client, message):
    if not await sd.is_user_exist(message.from_user.id):
        await sd.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(PIC_LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))

    buttons = [[
        InlineKeyboardButton("Hᴇʟᴩ" , callback_data="help") ,
        InlineKeyboardButton("Aʙᴏᴜᴛ" , callback_data="about"),
        InlineKeyboardButton("close" , callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text=f"Hello {message.from_user.mention}\n\nWelcome to the photo saver bot, click help button for how to use the bot",
        reply_markup = reply_markup ,
        parse_mode = enums.ParseMode.HTML
        )
@Client.on_message(filters.photo)
async def photo(client, message):
  try:
    photo = message.photo
    file_ids = photo.file_id
    user_id = message.from_user.id
    pic_saves = collection.find({"user_id": user_id})

    x = collection.insert_one({"user_id": user_id, "file_id": file_ids})
    await message.reply_text(f"insert {x}")
    await message.reply_text("Photo saved successfully")
  except Exception as e:
    await message.reply_text(e)

@Client.on_message(filters.command("pics"))
async def list_bots(client, message):
    try:
        user_id = message.from_user.id
        pic_saves = collection.find({"user_id": user_id})
        for pic_save in pic_saves:
            file_id = pic_save.get("file_id", "N/A")
            await client.send_cached_media(chat_id=user_id, file_id=file_id)

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command("del_one"))
async def del_many(client, message):
    try:
        user_id = message.from_user.id
        photo = message.reply_to_message.photo
        file_id = photo.file_id
        pic_exists = collection.find({"user_id": user_id})
        v = collection.delete_many({"file_id": file_id})
        await message.reply_text(v)
        await message.reply_text("Photo deleted successfully")
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command("del_many"))
async def delete(client, message):
  try:
    user_id = message.from_user.id
    pic_exists = collection.find({"user_id": user_id})
    for pic_exist in pic_exists:
        file_id = pic_exist.get("file_id", "N/A")
        y = collection.delete_many({"file_id": file_id})
        await message.reply_text(y)
    await message.reply_text("Photo deleted successfully")
  except Exception as e:
    await message.reply_text(e)

@Client.on_callback_query()
async def callback_handle(client, query):
    if query.data == 'help':
        buttons = [[
        InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='start') ,
        InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(text="Welcome to the photo manager bot. You can save, view, and delete your uploaded photos. Here are the commands:\n/pics - List your saved photos\n/del_one - Delete a specific photo. reply to the photo that you have sended.\n/del_many - Delete all your saved photos",reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'about':
         buttons = [[
             InlineKeyboardButton('Home' , callback_data='start') ,
             InlineKeyboardButton('close' , callback_data='close')
         ]]
         reply_markup = InlineKeyboardMarkup(buttons)
         await query.message.edit_text(text=ABOUT_TXT,reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'close':
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)
