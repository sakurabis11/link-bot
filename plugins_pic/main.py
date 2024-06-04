import pyrogram
from pyrogram import Client, filters, enums
import pymongo
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.types import *
from pyrogram.errors import *
from pymongo import MongoClient
import os
import asyncio
import random
import string
from utils import get_size
from Script import script
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from info import DATABASE_URI_2, DATABASE_NAME_2, LOG_CHANNEL, PIC_LOG_CHANNEL, ADMINS, S_CHANNEL, S_GROUP
from database_pic.pic_users_db import sd
from os import environ

ABOUT_TXT="""
✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a href='https://t.me/MrTG_Coder'>ᴍʀ.ʙᴏᴛ ᴛɢ</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>
✯ Mʏ Sᴇʀᴠᴇʀ: <a href='https://t.me/mrtgcoderbot'>ᴏʙᴀɴᴀɪ</a>
✯ Pʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: ᴠ2.0.106
✯ Mʏ ᴠᴇʀsɪᴏɴ: ᴠ4.5
"""

client = MongoClient(DATABASE_URI_2)
db = client[DATABASE_NAME_2]
collection = db["pic_db"]

@Client.on_message(filters.command('stats')  & filters.private)
async def get_stats(bot, message):
 try:
        user_id = message.from_user.id
        msg = await message.reply('Fetching stats..')
        total_users = await sd.total_users_count()
        totl_chats = await sd.total_chat_count()
        total_count = collection.count_documents({})
        user_count = collection.count_documents({"user_id": user_id})
        size = await sd.get_db_size()
        free = 536870912 - size
        size = get_size(size)
        free = get_size(free)
        await msg.edit(script.STATS_TXT.format(total_users , total_count , user_count , size , free))
 except Exception as e:
    await msg.edit(e)

@Client.on_message(filters.command('users') & filters.user(ADMINS)  & filters.private)
async def list_users(bot, message):
    msg = await message.reply('ɢᴇᴛᴛɪɴɢ ᴛʜᴇ ᴜsᴇʀs')
    users = await sd.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await msg.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
 try:
    if not await sd.is_user_exist(message.from_user.id):
        await sd.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(PIC_LOG_CHANNEL, script.LOG_TEXT_PI.format(message.from_user.id, message.from_user.mention, message.from_user.id))
    find_user_id = collection.find_one({"user_ids": message.from_user.id})
    if not find_user_id:
         await message.reply_text("you didn't create a storage for storing pic, so click on /create")
         return
    buttons = [[
        InlineKeyboardButton("Hᴇʟᴩ" , callback_data="help") ,
        InlineKeyboardButton("Aʙᴏᴜᴛ" , callback_data="about")
        ],[
        InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ' , url=S_CHANNEL) ,
        InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ' , url=S_GROUP)
        ],[
        InlineKeyboardButton("close" , callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text=f"Hello {message.from_user.mention}\n\nWelcome to the photo saver bot, click help button for how to use the bot",
        reply_markup = reply_markup ,
        parse_mode = enums.ParseMode.HTML
        )
    user_id = message.from_user.id
    existing_log_u = collection.find_one({"login": message.from_user.id})
    if not existing_log_u:
        await message.reply_text("You didn't login, so please login to access your stored pics")
        return
 except Exception as e:
    await message.reply_text(e)

@Client.on_message(filters.command("create") & filters.private)
async def create_pass(client:Client , message: Message):
    # details of user
    user_id = message.from_user.id
    user_f_name = message.from_user.first_name
    user_u_name = message.from_user.username or None
    find_user_id = collection.find_one({"user_ids": message.from_user.id})
    if find_user_id:
        await message.reply_text(
            "you already login, send ur id, username, password eg:- /login (ur id) (username) (password)")
        return
    a = await message.reply_text("creating ur username and password")
    letters = string.ascii_letters
    digits = string.digits

    desired_length = 10
    all_chars = ''.join(random.sample(letters , 5) + random.sample(digits , 5))

    username = ''.join(random.choice(all_chars) for _ in range(desired_length))
    password = ''.join(random.choice(all_chars) for _ in range(desired_length))
    print(f"username: {username}\n\npassword: {password}")

    z = await a.edit(
        f"user name: {username}\npassword: {password}\n\n<code>/login {user_id} {username} {password}</code>\n\nplease save this message to ur saved message because it will delete in 10 seconds")

    user_info = {
        "user_ids": user_id ,
        "username": username ,
        "password": password
    }
    if user_info:
        collection.insert_one(user_info)
        print(f"user_info: {user_info}")
        await message.reply_text("create successfully")
        await asyncio.sleep(8)
        await z.delete()
    else:
        await message.reply_text("Failed to connect, so please try again")

@Client.on_message(filters.command("login") & filters.private)
async def login_session(client: Client , message: Message):
  try:
    user_id = message.from_user.id

    existing_log_u = collection.find_one({"login": message.from_user.id})
    if existing_log_u:
        await message.reply_text("You already log in")
        return
    find_user_id = collection.find_one({"user_ids": message.from_user.id})
    if not find_user_id:
        await message.reply_text("you didn't create a storage for storing pic, so click on /create")
        return
    login = message.text.split(" " , 3)
    user_ids = int(login[1])
    username = login[2]
    password = login[3]
    await message.delete()
    if user_id != user_ids:
        await message.reply_text("The user id is incorrect, so please check again")

    existing_u_p = collection.find_one({"user_ids": user_id , "username": username , "password": password})
    if not existing_u_p:
        await message.reply_text("The password or username is wrong, so please send the correct username or password")
        return
    await message.reply_text("successfully logined")
    logged_in_users = collection.insert_one({"login": message.from_user.id})
  except IndexError:
      await message.reply_text("send ur id, username, password eg:- /login (ur id) (username) (password)")
  except Exception as e:
      await message.reply_text(e)

@Client.on_message(filters.command("logout") & filters.private)
async def logout(client:Client, message: Message):
    user_id = message.from_user.id

    find_user_id = collection.find_one({"user_ids": message.from_user.id})
    if not find_user_id:
        await message.reply_text("you didn't create a storage for storing pic, so click on /create")
        return

    existing_log_u = collection.find_one({"login": message.from_user.id})
    if not existing_log_u:
        await message.reply_text("You didn't login, so please login to access your stored pics")
        return
    if existing_log_u:
        collection.delete_one({"login": message.from_user.id})
        await message.reply_text("Successfully logged out!")

@Client.on_message(filters.command("show") & filters.private)
async def show(client: Client, message):
    user_id = message.from_user.id
    existing_u_p = collection.find_one({"user_ids": user_id})
    if not existing_u_p:
        await message.reply_text("you didn't create a storage for storing pic, so click on /create")
        return
    username = existing_u_p["username"]
    password = existing_u_p["password"]
    x=await message.reply_text(f"Your username is <code>{username}</code> and your password is <code>{password}</code>")
    await asyncio.sleep(10)
    await x.delete()

@Client.on_message(filters.command("delete") & filters.private)
async def delete_account(client: Client, message: Message):
  user_id = message.from_user.id

  find_user_id = collection.find_one({"user_ids": user_id})
  if not find_user_id:
      await message.reply_text("You don't have an account to delete. Please create one using /create")
      return

  # Confirmation before deletion
  confirmation_message = "Are you sure you want to delete your account? This action is irreversible.'yes' to confirm or 'no' to cancel."
  buttons = [[
      InlineKeyboardButton("yes" , callback_data="yess")
      ],[
      InlineKeyboardButton("no" , callback_data="noo")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(
      text=confirmation_message,
      reply_markup=reply_markup ,
      parse_mode=enums.ParseMode.HTML
  )

# <------------------------pic save----------------------------->

@Client.on_message(filters.photo & filters.private)
async def photo(client, message):
  try:
    user_id = message.from_user.id
    find_user_id = collection.find_one({"user_ids": message.from_user.id})
    if not find_user_id:
        await message.reply_text("you didn't create a storage for storing pic, so click on /create")
        return
    existing_log_u = collection.find_one({"login": message.from_user.id})
    if not existing_log_u:
        await message.reply_text("You didn't login, so please login to access your stored pics")
    else:
        photo = message.photo
        file_ids = photo.file_id
        unique_id = photo.file_unique_id
        
        pic_saves = collection.find_one({"user_id": user_id, "unique_id": unique_id})
        if pic_saves:
           await message.reply_text("This photo is already saved in your collection.")
           return
        collection.insert_one({"user_id": user_id, "unique_id": unique_id, "file_id": file_ids})

        await message.reply_text(f"Photo saved successfully\n\n")
        if message.from_user.username != None:
            await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=file_ids ,
                                           caption=f"Photo from @{message.from_user.username}")
        else:
            await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=file_ids ,
                                           caption=f"Photo from {message.from_user.mention} {message.from_user.first_name}")
  except PeerIdInvalid:
    pass
  except Exception as e:
    await message.reply_text(e)

@Client.on_message(filters.command("pics") & filters.private)
async def list_bots(client, message):
    try:
        user_id = message.from_user.id
        user_first = message.from_user.first_name
        user_user = message.from_user.username or None
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for storing pic, so click on /create")
            return
        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text("You didn't login, so please login to access your stored pics")
        else:
            photos = collection.find({"user_id": user_id})
            if not photos:
               await message.reply_text("You don't have any saved photos yet.")
               return
            for photo_info in photos:
                file_id = photo_info["file_id"]
                await client.send_cached_media(chat_id=user_id , file_id=file_id)

    except Exception as e:
        pass
        await client.send_message(PIC_LOG_CHANNEL, text=f"An error occurred: {e}\n\nFrom user id: {user_id}\nFrom user first name: {user_first}\nUsername: @{user_user}")

@Client.on_message(filters.command("id") & filters.private)
async def del_many(client, message):
    try:
        user_id = message.from_user.id
        await message.reply_text(f"ur id: {user_id}")
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command("del_one")  & filters.private)
async def del_many(client, message):
    try:
        user_id = message.from_user.id
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for storing pic, so click on /create")
            return
        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text("You didn't login, so please login to access your stored pics")
        else:
            photo = message.reply_to_message.photo
            unique_id = photo.file_unique_id
            user_id = message.from_user.id
            
            if collection.delete_one({"user_id": user_id , "unique_id": unique_id}):
                await message.reply_text("Photo deleted successfully!")
            else:
                await message.reply_text("Photo not found in your collection.")
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command("del_many")  & filters.private)
async def delete(client, message):
  try:
    user_id = message.from_user.id
    find_user_id = collection.find_one({"user_ids": message.from_user.id})
    if not find_user_id:
        await message.reply_text("you didn't create a storage for storing pic, so click on /create")
        return
    existing_log_u = collection.find_one({"login": message.from_user.id})
    if not existing_log_u:
        await message.reply_text("You didn't login, so please login to access your stored pics")
    else:
        collection.delete_many({"user_id": user_id})
        await message.reply_text("All your saved photos have been deleted.")
  except Exception as e:
    await message.reply_text(e)


@Client.on_callback_query()
async def callback_handle(client, query):
    if query.data == 'start':
        buttons = [[
        InlineKeyboardButton("Hᴇʟᴩ" , callback_data="help") ,
        InlineKeyboardButton("Aʙᴏᴜᴛ" , callback_data="about"),
        ],[
        InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ' , url=S_CHANNEL),
        InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ' , url=S_GROUP)
        ],[
        InlineKeyboardButton("close" , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(text=f"Hello {query.from_user.mention}\n\nWelcome to the photo saver bot, click help button for how to use the bot",reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
    
    elif query.data == 'help':
        buttons = [[
        InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='start') ,
        InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(text="Welcome to the photo saver bot. You can save, view, and delete your uploaded photos. Here are the commands:\n\n/pics - List your saved photos\n/del_one - Delete a specific photo. reply to the photo that you have sended.\n/del_many - Delete all your saved photos",reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'about':
         buttons = [[
             InlineKeyboardButton('Home' , callback_data='start') ,
             InlineKeyboardButton('close' , callback_data='close')
         ]]
         reply_markup = InlineKeyboardMarkup(buttons)
         await query.message.edit_text(text=ABOUT_TXT,reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'yess':
         user_id = query.from_user.id
         collection.delete_one({"user_ids": user_id})
         collection.delete_many({"user_id": user_id})
         collection.delete_one({"login": user_id})
         await client.send_message(user_id , text="Your account has been deleted successfully.")
         await query.message.delete()
         edited_keyboard = InlineKeyboardMarkup([])
         await query.answer()
         await query.message.edit_reply_markup(edited_keyboard)

    elif query.data == 'noo':
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)
     
    elif query.data == 'close':
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)
