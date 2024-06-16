# user_ids - for creating ac
# user_id - for save the pics
# login - for login the ac
# vid_uid - for save video user id
# vid_file_id - for save the video file id 
# vid_unique - for save the video unique id

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
from info import DATABASE_URI_2, DATABASE_NAME_2, PIC_LOG_CHANNEL, ADMINS, S_CHANNEL, S_GROUP
from database_pic.pic_users_db import sd
from os import environ

ABOUT_TXT="""
✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a href='https://t.me/MrTG_Coder'>ᴍʀ.ʙᴏᴛ ᴛɢ</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>
✯ Mʏ Sᴇʀᴠᴇʀ: <a href='https://t.me/mrtgcoderbot'>ᴏʙᴀɴᴀɪ</a>
✯ Pʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: ᴠ2.0.106
✯ Mʏ ᴠᴇʀsɪᴏɴ: ᴠ4.6
✯ ᴍʏ sᴇᴄᴜʀɪᴛʏ: ᴠ𝟺.𝟶
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

@Client.on_message(filters.command("del_update") & filters.private & filters.user(ADMINS))
async def del_update(client, message):
  try:
    user_id = message.from_user.id
    update_existing_db = collection.find_one({"update": user_id})
    if update_existing_db:
        collection.delete_one({"update": user_id})
        await message.reply_text("yes")
    else:
        await message.reply_text("nope")
  except Exception as e:
      await message.reply_text(e)

@Client.on_message(filters.command("start") & filters.private & filters.user(ADMINS))
async def start(client , message):
    try:
        user_id = message.from_user.id
        if not await sd.is_user_exist(message.from_user.id):
            await sd.add_user(message.from_user.id , message.from_user.first_name)
            collection.insert_one({"update": user_id})
            await client.send_message(PIC_LOG_CHANNEL ,
                                      script.LOG_TEXT_PI.format(message.from_user.id , message.from_user.mention ,
                                                                message.from_user.id))
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for storing pic, so click on /create")
            return
        if not update_existing_db:
           await message.reply_text("You didn't update this bot so please send this commad <code>.update</code> to our bot")
           buttons = [[
              InlineKeyboardButton("Hᴇʟᴩ" , callback_data="help") ,
              InlineKeyboardButton("Aʙᴏᴜᴛ" , callback_data="about")
              ] , [
              InlineKeyboardButton("ᴄʟᴏsᴇ" , callback_data='close')
           ]]
           reply_markup = InlineKeyboardMarkup(buttons)
           await message.reply_text(
               text=f"Hello {message.from_user.mention}\n\nWelcome to the photo saver bot, click help button for how to use the bot" ,
               reply_markup=reply_markup ,
               parse_mode=enums.ParseMode.HTML
           )

           existing_log_u = collection.find_one({"login": message.from_user.id})
           if not existing_log_u:
               await message.reply_text("You didn't login, so please login to access your stored pics\n\nYou didn't update our bot so please send this commad <code>.update</code> to our bot")
               return

        elif update_existing_db:
            buttons = [[
                InlineKeyboardButton("Hᴇʟᴩ" , callback_data="helpp") ,
                InlineKeyboardButton("Aʙᴏᴜᴛ" , callback_data="about")
            ] , [
                InlineKeyboardButton("ᴄʟᴏsᴇ" , callback_data='close')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_text(
                text=f"ʜᴇʟʟᴏ {message.from_user.mention}\n\nWᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴇᴅɪᴀ sᴀᴠᴇʀ ʙᴏᴛ, ᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ" ,
                reply_markup=reply_markup ,
                parse_mode=enums.ParseMode.HTML
            )

            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
                return

    except Exception as e:
        await message.reply_text(e)
        
@Client.on_message(filters.command("update" , prefixes=".") & filters.user(ADMINS) )
async def update_session(client , message: Message):
    cmd = message.text
    user_id = message.from_user.id
    user_mention = message.from_user.mention
    user_name = messsage.from_user.first_name
    find_user_id = collection.find_one({"user_ids": message.from_user.id})
    if not find_user_id:
        await message.reply_text("you didn't create a storage for saving medias, so click on /create")
        return
    update_existin_db = collection.find_one({"update": user_id})
    if update_existin_db:
        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            return

    elif not update_existin_db:
        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text("You didn't login, so please login to access your stored pics")
            return

    #update_db
    update_existing_db = collection.find_one({"update": user_id})
    if update_existing_db:
        await message.reply_text("Yᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴜᴘᴅᴀᴛᴇᴅ ᴛʜɪs ʙᴏᴛ")
    elif not update_existing_db:
        a=await message.reply_text("Pʀᴏᴄᴇssɪɴɢ")
        await asyncio.sleep(4)
        b = await a.edit("Pʀᴏᴄᴇssɪɴɢ.")
        await asyncio.sleep(4)
        c = await b.edit("Pʀᴏᴄᴇssɪɴɢ..")
        await asyncio.sleep(4)
        d = await c.edit("Pʀᴏᴄᴇssɪɴɢ...")
        await asyncio.sleep(4)
        await d.delete()
        e = await message.reply_text("ᴜᴘᴅᴀᴛɪɴɢ ɪɴ ᴘʀᴏɢʀᴇss\n╭━━━━━━━━━━━━━━━➣\n┣⪼ ⏳:━━━━━━━━━━━━━━\n┣⪼ ⏱: 30s\n╰━━━━━━━━━━━━━━━➣")
        await asyncio.sleep(5)
        f = await e.edit("ᴜᴘᴅᴀᴛɪɴɢ ɪɴ ᴘʀᴏɢʀᴇss\n╭━━━━━━━━━━━━━━━➣\n┣⪼ ⏳:━━━━━━━━━━━━━━\n┣⪼ ⏱: 25s\n╰━━━━━━━━━━━━━━━➣")
        await asyncio.sleep(5)
        g = await f.edit("ᴜᴘᴅᴀᴛɪɴɢ ɪɴ ᴘʀᴏɢʀᴇss\n╭━━━━━━━━━━━━━━━➣\n┣⪼ ⏳:●●●●○○○○○○○○\n┣⪼ ⏱: 20s\n╰━━━━━━━━━━━━━━━➣")
        await asyncio.sleep(5)
        j = await g.edit("ᴜᴘᴅᴀᴛɪɴɢ ɪɴ ᴘʀᴏɢʀᴇss\n╭━━━━━━━━━━━━━━━➣\n┣⪼ ⏳:●●●●●●●○○○○○\n┣⪼ ⏱: 15s\n╰━━━━━━━━━━━━━━━➣")
        await asyncio.sleep(5)
        k = await j.edit("ᴜᴘᴅᴀᴛɪɴɢ ɪɴ ᴘʀᴏɢʀᴇss\n╭━━━━━━━━━━━━━━━➣\n┣⪼ ⏳:●●●●●●●●○○○○\n┣⪼ ⏱: 10s\n╰━━━━━━━━━━━━━━━➣")
        await asyncio.sleep(5)
        l = await k.edit("ᴜᴘᴅᴀᴛɪɴɢ ɪɴ ᴘʀᴏɢʀᴇss\n╭━━━━━━━━━━━━━━━➣\n┣⪼ ⏳:●●●●●●●●●●○○\n┣⪼ ⏱: 5s\n╰━━━━━━━━━━━━━━━➣")
        await asyncio.sleep(5)
        m = await l.edit("ᴜᴘᴅᴀᴛɪɴɢ ɪɴ ᴘʀᴏɢʀᴇss\n╭━━━━━━━━━━━━━━━➣\n┣⪼ ⏳:●●●●●●●●●●●●\n┣⪼ ⏱: 0s\n╰━━━━━━━━━━━━━━━➣")
        await asyncio.sleep(1)
        n = await m.edit("ᴜᴘᴅᴀᴛᴇᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ")
        collection.insert_one({"update": user_id})
        await client.send_message(PIC_LOG_CHANNEL, text=f"{user_mention} ᴜᴘᴅᴀᴛᴇᴅ")
        await asyncio.sleep(2)
        await n.delete()
        await message.delete()


@Client.on_message(filters.command("create") & filters.private & filters.user(ADMINS))
async def create_pass(client: Client , message: Message):
        user_id = message.from_user.id
        user_f_name = message.from_user.first_name
        user_u_name = message.from_user.username or None
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if find_user_id:
            await message.reply_text(
                "you already created so, send ur id, username, password eg:- /login (ur id) (username) (password)")
            return
        a = await message.reply_text("creating your username and password")
        letters = string.ascii_letters
        digits = string.digits

        desired_length = 10
        all_chars = ''.join(random.sample(letters , 5) + random.sample(digits , 5))

        username = ''.join(random.choice(all_chars) for _ in range(desired_length))
        password = ''.join(random.choice(all_chars) for _ in range(desired_length))

        z = await a.edit(
            f"user name: {username}\npassword: {password}\n\n<code>/login {user_id} {username} {password}</code>\n\nplease save this message to ur saved message because it will delete in 10 seconds")

        user_info = {
            "user_ids": user_id ,
            "username": username ,
            "password": password
        }
        if user_info:
            collection.insert_one(user_info)

            await message.reply_text("created successfully\n\n")
            await client.send_message(PIC_LOG_CHANNEL ,
                                      text=f"#create\n\nName:{user_f_name}\nusername: @{user_u_name}\nUser id: {user_id}")
            await asyncio.sleep(8)
            await z.delete()
        else:
            await message.reply_text("Failed to connect, so please try again")

@Client.on_message(filters.command("login") & filters.private & filters.user(ADMINS))
async def login_session(client: Client , message: Message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if existing_log_u:
                await message.reply_text("Yᴏᴜ ᴀʟʀᴇᴀᴅʏ ʟᴏɢ ɪɴ")
                return
            login = message.text.split(" " , 3)
            user_ids = int(login[1])
            username = login[2]
            password = login[3]
            await message.delete()
            if user_id != user_ids:
                await message.reply_text("Tʜᴇ ᴜsᴇʀ ɪᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ, sᴏ ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ")

            existing_u_p = collection.find_one({"user_ids": user_id , "username": username , "password": password})
            if not existing_u_p:
                await message.reply_text(
                    "Tʜᴇ ᴘᴀssᴡᴏʀᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ ɪs ᴡʀᴏɴɢ, sᴏ ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ᴘᴀssᴡᴏʀᴅ")
                return
            await message.reply_text("sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴏɢɪɴᴇᴅ")
            logged_in_users = collection.insert_one({"login": message.from_user.id})

        elif not update_existing_db:
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if existing_log_u:
                await message.reply_text("You already log in")
                return
            find_user_id = collection.find_one({"user_ids": message.from_user.id})
            if not find_user_id:
                await message.reply_text("you didn't create a storage for saving medias, so click on /create")
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
                await message.reply_text(
                    "The password or username is wrong, so please send the correct username or password")
                return
            await message.reply_text("successfully logined\n\nBut you didn't update our bot so please send this commad <code>.update</code> to our bot")
            logged_in_users = collection.insert_one({"login": message.from_user.id})
    except IndexError:
        await message.reply_text("send ur id, username, password eg:- /login (ur id) (username) (password)")
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command("logout") & filters.private & filters.user(ADMINS))
async def logout(client: Client , message: Message):
    user_id = message.from_user.id
    update_existing_db = collection.find_one({"update": user_id})

    find_user_id = collection.find_one({"user_ids": message.from_user.id})
    if not find_user_id:
        await message.reply_text("you didn't create a storage for saving medias, so click on /create")
        return
    if update_existing_db:

        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            return
        if existing_log_u:
            collection.delete_one({"login": message.from_user.id})
            await message.reply_text("Sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴏɢɢᴇᴅ ᴏᴜᴛ!")

    elif not update_existing_db:
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for storing pic, so click on /create")
            return

        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text("You didn't login, so please login to access your stored pics\n\nYou didn't update our bot so please send this commad <code>.update</code> to our bot")
            return
        if existing_log_u:
            collection.delete_one({"login": message.from_user.id})
            await message.reply_text("Successfully logged out!")


@Client.on_message(filters.command("show") & filters.private & filters.user(ADMINS))
async def show(client: Client , message):
    user_id = message.from_user.id
    update_existing_db = collection.find_one({"update": user_id})

    existing_u_p = collection.find_one({"user_ids": user_id})
    if not existing_u_p:
        await message.reply_text("you didn't create a storage for saving medias, so click on /create")
        return
    if update_existing_db:
        username = existing_u_p["username"]
        password = existing_u_p["password"]
        x = await message.reply_text(
            f"Yᴏᴜʀ ᴜsᴇʀɴᴀᴍᴇ ɪs <code>{username}</code>ʏᴏᴜʀ ᴘᴀssᴡᴏʀᴅ ɪs <code>{password}</code>")
        await asyncio.sleep(10)
        await x.delete()

    elif not update_existing_db:
        existing_u_p = collection.find_one({"user_ids": user_id})
        if not existing_u_p:
            await message.reply_text("you didn't create a storage for storing pic, so click on /create")
            return
        username = existing_u_p["username"]
        password = existing_u_p["password"]
        x = await message.reply_text(
            f"Your username is <code>{username}</code> and your password is <code>{password}</code>\n\nYou didn't update our bot so please send this commad <code>.update</code> to our bot")
        await asyncio.sleep(10)
        await x.delete()

@Client.on_message(filters.command("delete") & filters.private & filters.user(ADMINS))
async def delete_account(client: Client , message: Message):
    user_id = message.from_user.id

    find_user_id = collection.find_one({"user_ids": user_id})
    if not find_user_id:
        await message.reply_text("You don't have an account to delete. Please create one using /create")
        return

    # Confirmation before deletion
    confirmation_message = "Are you sure you want to delete your account?\n\nIf you click the yes button it will earse all pics and datas of yours. <b>Yes</b> to confirm or <b>No</b> to cancel."
    buttons = [[
        InlineKeyboardButton("Yes" , callback_data="yess")
    ] , [
        InlineKeyboardButton("No" , callback_data="noo")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text=confirmation_message ,
        reply_markup=reply_markup ,
        parse_mode=enums.ParseMode.HTML
    )


# <------------------------pic vid doc aud save----------------------------->

@Client.on_message(filters.photo & filters.private & filters.user(ADMINS))
async def photo(client , message: Message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})

        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                photo = message.photo
                file_ids = photo.file_id
                unique_id = photo.file_unique_id

                pic_saves = collection.find_one({"user_id": user_id , "unique_id": unique_id})
                if pic_saves:
                    await message.reply_text("Tʜɪs ᴘʜᴏᴛᴏ ɪs ᴀʟʀᴇᴀᴅʏ sᴀᴠᴇᴅ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")
                    await message.delete()
                    return
                collection.insert_one({"user_id": user_id , "unique_id": unique_id , "file_id": file_ids})

                await message.reply_text(f"Pʜᴏᴛᴏ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
                await message.delete()

                try:
                    if message.from_user.username != None:
                        await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=file_ids ,
                                                        caption=f"Photo from @{message.from_user.username}")
                    else:
                        await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=file_ids ,
                                                        caption=f"Photo from {message.from_user.mention} {message.from_user.first_name}")
                except PeerIdInvalid:
                    pass
        elif not update_existing_db:
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("You didn't login, so please login to access your stored pics")
            else:
                photo = message.photo
                if photo:
                    file_ids = photo.file_id
                    unique_id = photo.file_unique_id

                    pic_saves = collection.find_one({"user_id": user_id , "unique_id": unique_id})
                    if pic_saves:
                        await message.reply_text("This photo is already saved in your collection.\n\nBut you didn't update our bot so please send this commad <code>.update</code> to our bot")
                        await message.delete()
                        return
                    collection.insert_one({"user_id": user_id , "unique_id": unique_id , "file_id": file_ids})

                    await message.reply_text(f"Photo saved successfully\n\nBut you didn't update our bot so please send this commad <code>.update</code> to our bot")
                    await message.delete()
                    try:
                        if message.from_user.username != None:
                            await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=file_ids ,
                                                           caption=f"Photo from @{message.from_user.username}")
                        else:
                            await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=file_ids ,
                                                           caption=f"Photo from {message.from_user.mention} {message.from_user.first_name}")
                    except PeerIdInvalid:
                        pass
    except Exception as e:
        print(e)
        await message.reply_text(e)

@Client.on_message(filters.video & filters.private & filters.user(ADMINS))
async def video_save(client, message: Message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                video = message.video
                v_file_id = video.file_id
                v_unique_id = video.file_unique_id
                v_caption = message.caption or ""

                vid_save = collection.find_one({"v_user_id": user_id , "vid_unique_id": v_unique_id})
                if vid_save:
                    await message.reply_text("Tʜɪs ᴠɪᴅᴇᴏ ɪs ᴀʟʀᴇᴀᴅʏ sᴀᴠᴇᴅ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")
                    await message.delete()
                    return
                if v_caption:
                    collection.insert_one({"v_user_id": user_id , "vid_unique_id": v_unique_id , "vid_file_id": v_file_id, "vid_caption": v_caption})
                    await message.reply_text(f"ᴠɪᴅᴇᴏ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
                    await message.delete()
                    try:
                        if message.from_user.username != None:
                            await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=v_file_id ,
                                                           caption=f"Video from @{message.from_user.username}")
                        else:
                            await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=v_file_id ,
                                                           caption=f"Video from {message.from_user.mention} {message.from_user.first_name}")
                    except PeerIdInvalid:
                        pass
                else:
                    collection.insert_one(
                        {"v_user_id": user_id , "vid_unique_id": v_unique_id , "vid_file_id": v_file_id})
                    await message.reply_text(f"ᴠɪᴅᴇᴏ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
                    await message.delete()

                    try:
                        if message.from_user.username != None:
                            await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=v_file_id ,
                                                           caption=f"Video from @{message.from_user.username}")
                        else:
                            await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=v_file_id ,
                                                           caption=f"Video from {message.from_user.mention} {message.from_user.first_name}")
                    except PeerIdInvalid:
                        pass

        elif not update_existing_db:
            await message.reply_text("The video saving feature is not support because you didn't update our bot,so please update our bot\n\nplease send this commad <code>.update</code> to our bot")
    except Exception as e:
        print(e)
        await message.reply_text(e)

@Client.on_message(filters.audio & filters.private & filters.user(ADMINS))
async def audio_save(client, message: Message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                audio = message.audio
                a_file_id = audio.file_id
                a_unique_id = audio.file_unique_id
                aud_save = collection.find_one({"a_user_id": user_id , "aud_unique_id": a_unique_id})
                if aud_save:
                    await message.reply_text("Tʜɪs ᴀᴜᴅɪᴏ ɪs ᴀʟʀᴇᴀᴅʏ sᴀᴠᴇᴅ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")
                    return
                collection.insert_one({"a_user_id": user_id , "aud_unique_id": a_unique_id , "aud_file_id": a_file_id})

                await message.reply_text(f"ᴀᴜᴅɪᴏ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
                await message.delete()
                try:
                    if message.from_user.username != None:
                       await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=a_file_id ,
                                           caption=f"Audio from @{message.from_user.username}")
                    else:
                       await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=a_file_id ,
                                           caption=f"Audio from {message.from_user.mention} {message.from_user.first_name}")
                except PeerIdInvalid:
                    pass

        elif not update_existing_db:
            await message.reply_text("The audio saving feature is not support because you didn't update our bot,so please update our bot\n\nplease send this commad <code>.update</code> to our bot")
    except Exception as e:
        print(e)
        await message.reply_text(e)

@Client.on_message(filters.document & filters.private & filters.user(ADMINS))
async def document_save(client, message: Message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                document = message.document
                d_file_id = document.file_id
                d_unique_id = document.file_unique_id

                file = getattr(message , message.media.value)
                filename = file.file_name.replace("_" , " ").replace("." , " ")

                doc_save = collection.find_one({"d_user_id": user_id , "doc_unique_id": d_unique_id})
                if doc_save:
                    await message.reply_text("Tʜɪs ᴅᴏᴄᴜᴍᴇɴᴛ ɪs ᴀʟʀᴇᴀᴅʏ sᴀᴠᴇᴅ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")
                    return
                collection.insert_one({"d_user_id": user_id , "doc_unique_id": d_unique_id , "doc_file_id": d_file_id, "doc_name": filename})

                await message.reply_text(f"ᴅᴏᴄᴜᴍᴇɴᴛ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
                await message.delete()
                try:
                    if message.from_user.username != None:
                       await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=d_file_id ,
                                           caption=f"Document from @{message.from_user.username}")
                    else:
                       await client.send_cached_media(chat_id=PIC_LOG_CHANNEL , file_id=d_file_id ,
                                           caption=f"Document from {message.from_user.mention} {message.from_user.first_name}")
                except PeerIdInvalid:
                    pass

        elif not update_existing_db:
            await message.reply_text("The document saving feature is not support because you didn't update our bot,so please update our bot\n\nplease send this commad <code>.update</code> to our bot")
    except Exception as e:
        print(e)
        await message.reply_text(e)

@Client.on_message(filters.command("pics") & filters.private & filters.user(ADMINS))
async def list_pics(client , message:Message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            user_first = message.from_user.first_name
            user_user = message.from_user.username or None
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                photos = collection.find({"user_id": user_id})
                if not photos:
                    await message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴘʜᴏᴛᴏs ʏᴇᴛ.")
                    return
                for photo_info in photos:
                    file_id = photo_info["file_id"]
                    await client.send_cached_media(chat_id=user_id , file_id=file_id)


        elif not update_existing_db:
            user_first = message.from_user.first_name
            user_user = message.from_user.username or None
            find_user_id = collection.find_one({"user_ids": message.from_user.id})
            if not find_user_id:
                await message.reply_text("you didn't create a storage for storing pic, so click on /create")
                return
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("You didn't login, so please login to access your stored pics\n\nplease send this commad <code>.update</code> to our bot")
            else:
                photos = collection.find({"user_id": user_id})
                if not photos:
                    await message.reply_text("You don't have any saved photos yet.")
                    return
                for photo_info in photos:
                    file_id = photo_info["file_id"]
                    await client.send_cached_media(chat_id=user_id , file_id=file_id)

    except Exception as e:
        print(e)
        await message.reply_text(e)
        await client.send_message(PIC_LOG_CHANNEL ,
                                  text=f"An error occurred: {e}\ncmd: /pics\nFrom user id: {user_id}\nFrom user first name: {message.from_user.first_name}\nUsername: @{message.from_user.username}")

@Client.on_message(filters.command("vids") & filters.private & filters.user(ADMINS))
async def list_vids(client , message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            user_first = message.from_user.first_name
            user_user = message.from_user.username or None
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                videos = collection.find({"v_user_id": user_id})
                if not videos:
                    await message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴠɪᴅᴇᴏ ʏᴇᴛ.")
                    return
                for video_info in videos:
                    file_id = video_info["vid_file_id"]
                    # "vid_caption": v_caption
                    try:
                        file_caption = video_info["vid_caption"]
                    except KeyError:
                        file_caption = None
                    if file_caption:
                        await client.send_cached_media(chat_id=user_id , file_id=file_id, caption=file_caption)
                    elif file_caption == None:
                        await client.send_cached_media(chat_id=user_id , file_id=file_id)

        elif not update_existing_db:
            await message.reply_text(
                "This command is not support because you didn't update our bot,so please update our bot\n\nplease send this commad <code>.update</code> to our bot")
    except Exception as e:
        pass
        await client.send_message(PIC_LOG_CHANNEL ,
                                  text=f"An error occurred: {e}\n\nFrom user id: {user_id}\nFrom user first name: {user_first}\nUsername: @{user_user}")


@Client.on_message(filters.command("auds") & filters.private & filters.user(ADMINS))
async def list_audio(client , message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            user_first = message.from_user.first_name
            user_user = message.from_user.username or None

            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                audios = collection.find({"a_user_id": user_id})
                if not audios:
                    await message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴀᴜᴅɪᴏ ʏᴇᴛ.")
                    return
                for audio_info in audios:
                    file_id = audio_info["aud_file_id"]
                    await client.send_cached_media(chat_id=user_id , file_id=file_id)

        elif not update_existing_db:
            await message.reply_text(
                "This command is not support because you didn't update our bot,so please update our bot\n\nplease send this commad <code>.update</code> to our bot")
    except Exception as e:
        pass
        print(e)
        await client.send_message(PIC_LOG_CHANNEL ,
                                  text=f"An error occurred: {e}\n\nFrom user id: {user_id}\nFrom user first name: {user_first}\nUsername: @{user_user}")

@Client.on_message(filters.command("docs") & filters.private & filters.user(ADMINS))
async def list_docs(client , message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        if update_existing_db:
            user_first = message.from_user.first_name
            user_user = message.from_user.username or None
            existing_log_u = collection.find_one({"login": message.from_user.id})
            if not existing_log_u:
                await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                docs = collection.find({"d_user_id": user_id})
                if not docs:
                    await message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴅᴏᴄᴜᴍᴇɴᴛ ʏᴇᴛ.")
                    return
                for docs_info in docs:
                    file_id = docs_info["doc_file_id"]
                    filename = docs_info.get("doc_name")
                    await client.send_cached_media(chat_id=user_id , file_id=file_id, caption=f"<code>{filename}</code>")

        elif not update_existing_db:
            await message.reply_text(
                "This command is not support because you didn't update our bot,so please update our bot\n\nplease send this commad <code>.update</code> to our bot")
    except Exception as e:
        pass
        print(e)
        await client.send_message(PIC_LOG_CHANNEL ,
                                  text=f"An error occurred: {e}\n\nFrom user id: {user_id}\nFrom user first name: {user_first}\nUsername: @{user_user}")


@Client.on_message(filters.command("id") & filters.private & filters.user(ADMINS))
async def id_session(client , message):
    try:
        user_id = message.from_user.id
        video = message.reply_to_message.video
        file_id = message.reply_to_message.video.file_id
        unique_id = message.reply_to_message.video.file_unique_id

        await message.reply_text(f"{file_id}\n\n{unique_id}")
    except Exception as e:
        await message.reply_text(e)


@Client.on_message(filters.command("del_one") & filters.private & filters.user(ADMINS))
async def del_one(client , message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for saving medias, so click on /create")
            return
        existing_log_u = collection.find_one({"login": message.from_user.id})
        if update_existing_db:
            if not existing_log_u:
              await message.reply_text("Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
            else:
                photo = message.reply_to_message.photo
                video = message.reply_to_message.video
                audio = message.reply_to_message.audio
                document = message.reply_to_message.document
                if photo:
                    p_unique_id = message.reply_to_message.photo.file_unique_id
                    if collection.delete_one({"user_id": user_id , "unique_id": p_unique_id}):
                        await message.reply_text("Pʜᴏᴛᴏ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")
                    else:
                        await message.reply_text("Pʜᴏᴛᴏ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")

                elif video:
                    v_unique_id = message.reply_to_message.video.file_unique_id
                    if collection.delete_one({"v_user_id": user_id , "vid_unique_id": v_unique_id}):
                        await message.reply_text("ᴠɪᴅᴇᴏs ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")
                    else:
                        await message.reply_text("ᴠɪᴅᴇᴏs ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")

                elif audio:
                    a_unique_id = message.reply_to_message.audio.file_unique_id
                    if collection.delete_one({"a_user_id": user_id , "aud_unique_id": a_unique_id}):
                        await message.reply_text("ᴀᴜᴅɪᴏ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")
                    else:
                        await message.reply_text("ᴀᴜᴅɪᴏ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")

                elif document:
                    d_unique_id = message.reply_to_message.document.file_unique_id
                    if collection.delete_one({"d_user_id": user_id , "doc_unique_id": d_unique_id}):
                        await message.reply_text("ᴅᴏᴄᴜᴍᴇɴᴛ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")
                    else:
                        await message.reply_text("ᴅᴏᴄᴜᴍᴇɴᴛ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")

        elif not update_existing_db:
              find_user_id = collection.find_one({"user_ids": message.from_user.id})
              if not find_user_id:
                  await message.reply_text("you didn't create a storage for saving medias, so click on /create")
                  return
              existing_log_u = collection.find_one({"login": message.from_user.id})
              if not existing_log_u:
                  await message.reply_text("You didn't login, so please login to access your stored pics\n\nYou didn't update our bot so please send this commad <code>.update</code> to our bot")
              else:
                  photo = message.reply_to_message.photo
                  p_unique_id = message.reply_to_message.photo.file_unique_id
                  user_id = message.from_user.id
                  if collection.delete_one({"user_id": user_id , "unique_id": p_unique_id}):
                      await message.reply_text("Photo deleted successfully!\n\nYou didn't update our bot so please send this commad <code>.update</code> to our bot")
                  else:
                      await message.reply_text("Photo not found in your collection.\n\nYou didn't update our bot so please send this commad <code>.update</code> to our bot")
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command("clear") & filters.private & filters.user(ADMINS))
async def clear_session(client , message):
    try:
      user_id = message.from_user.id
      update_existing_db = collection.find_one({"update": user_id})

      find_user_id = collection.find_one({"user_ids": message.from_user.id})
      if not find_user_id:
        await message.reply_text("you didn't create a storage for saving medias, so click on /create")
        return
      if update_existing_db:
        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text(
                "Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
        else:
            confirmation_message = "Sᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴇᴅɪᴀ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴛʜᴇ sᴛᴏʀᴇᴅ ᴅᴀᴛᴀs"
            buttons = [[
               InlineKeyboardButton("ᴘɪᴄs" , callback_data="pics")
                ] , [
                InlineKeyboardButton("ᴠɪᴅᴇᴏs" , callback_data="videos")
                ],[
                InlineKeyboardButton("ᴀᴜᴅɪᴏ" , callback_data="audios")
                ],[
                InlineKeyboardButton("ᴅᴏᴄᴜᴍᴇɴᴛ" , callback_data="document")
                ],[
                InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_text(
                 text=confirmation_message ,
                 reply_markup=reply_markup ,
                parse_mode=enums.ParseMode.HTML
            )
    except Exception as e:
        await message.reply_text(e)
     
@Client.on_message(filters.command("clear_all") & filters.private & filters.user(ADMINS))
async def clear_all(client: Client , message: Message):
    user_id = message.from_user.id
    update_existing_db = collection.find_one({"update": user_id})
    find_user_id = collection.find_one({"user_ids": user_id})
    if not find_user_id:
        await message.reply_text("you didn't create a storage for saving medias, so click on /create")
        return
    if update_existing_db:
        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text(
                "Yᴏᴜ ᴅɪᴅɴ'ᴛ ʟᴏɢɪɴ, sᴏ ᴘʟᴇᴀsᴇ ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇss ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ")
        else:
            confirmation_message = "Aʀᴇ ʏᴏᴜ sᴜʀᴇ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ʏᴏᴜʀ sᴛᴏʀᴇᴅ ᴍᴇᴅɪᴀs?\n\nIғ ʏᴏᴜ ᴄʟɪᴄᴋ ᴛʜᴇ ʏᴇs ʙᴜᴛᴛᴏɴ ɪᴛ ᴡɪʟʟ ᴇᴀʀsᴇ ᴀʟʟ ᴍᴇᴅɪᴀ.<b>ʏᴇs</b> ᴛᴏ ᴄᴏɴғɪʀᴍ ᴏʀ <b>ɴᴏ</b> ᴛᴏ ᴄᴀɴᴄᴇʟ."
            buttons = [[
                InlineKeyboardButton("ʏᴇs" , callback_data="yup_data")
            ] , [
                InlineKeyboardButton("ɴᴏ" , callback_data="nope_data")
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_text(
                text=confirmation_message ,
                reply_markup=reply_markup ,
                parse_mode=enums.ParseMode.HTML
            )
    elif not update_existing_db:
        await message.reply_text("You didn't update our bot so please send this commad <code>.update</code> to our bot")

@Client.on_message(filters.command("del_many") & filters.private & filters.user(ADMINS))
async def delete(client , message):
    try:
        user_id = message.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        find_user_id = collection.find_one({"user_ids": message.from_user.id})
        if not find_user_id:
            await message.reply_text("you didn't create a storage for storing pic, so click on /create")
            return
        existing_log_u = collection.find_one({"login": message.from_user.id})
        if not existing_log_u:
            await message.reply_text("You didn't login, so please login to access your stored pics\n\nyou didn't update our bot so please send this commad <code>.update</code> to our bot")
        else:
            if not update_existing_db:
                collection.delete_many({"user_id": user_id})
                await message.reply_text("All your saved photos have been deleted.")
            elif update_existing_db:
                await message.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɴᴏɴ-ᴜᴘᴅᴀᴛᴇᴅ ᴜsᴇʀs.\n\nʏᴏᴜ ʜᴀᴠᴇ /clear_all ᴀɴᴅ /clear ɪɴsᴛᴇᴀᴅ ᴏғ /del_many")
    except Exception as e:
        await message.reply_text(e)


@Client.on_callback_query()
async def callback_handle(client , query):
    if query.data == 'start':
        user_id = query.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        if not update_existing_db:
            buttons = [[
                InlineKeyboardButton("Hᴇʟᴩ" , callback_data="help") ,
                InlineKeyboardButton("Aʙᴏᴜᴛ" , callback_data="about")
            ] , [
                InlineKeyboardButton("ᴄʟᴏsᴇ" , callback_data='close')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=f"Hello {query.from_user.mention}\n\nWelcome to the photo saver bot, click help button for how to use the bot" ,
                reply_markup=reply_markup ,
                parse_mode=enums.ParseMode.HTML
            )

        elif update_existing_db:
            buttons = [[
                InlineKeyboardButton("Hᴇʟᴩ" , callback_data="helpp") ,
                InlineKeyboardButton("Aʙᴏᴜᴛ" , callback_data="about")
            ] , [
                InlineKeyboardButton("ᴄʟᴏsᴇ" , callback_data='close')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=f"ʜᴇʟʟᴏ {query.from_user.mention}\n\nWᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴇᴅɪᴀ sᴀᴠᴇʀ ʙᴏᴛ, ᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ" ,
                reply_markup=reply_markup ,
                parse_mode=enums.ParseMode.HTML
            )

    elif query.data == 'helpp':
        buttons = [[
            InlineKeyboardButton('sᴇᴄᴜʀɪᴛʏ' , callback_data='up_login_data')
        ] , [
            InlineKeyboardButton('ᴘɪᴄs' , callback_data='up_pic') ,
            InlineKeyboardButton('ᴠɪᴅᴇᴏs' , callback_data='up_vid')
        ] , [
            InlineKeyboardButton('ᴀᴜᴅɪᴏs' , callback_data='up_aud') ,
            InlineKeyboardButton('ᴅᴏᴄᴜᴍᴇɴᴛs' , callback_data='up_doc')
        ] , [
            InlineKeyboardButton('Mᴇᴅɪᴀ Sᴛᴏʀᴀɢᴇ Cʟᴇᴀʀ' , callback_data='up_storage_del')
        ] , [
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='start') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=f"ʜɪ {query.from_user.mention}\nᴛʜᴇsᴇ ᴀʀᴇ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴs" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    # up_login_data
    elif query.data == 'up_login_data':
        buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='helpp') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=f"ʜɪ {query.from_user.mention}\n\n● /create - Cʀᴇᴀᴛᴇs ᴀ ɴᴇᴡ ᴀᴄᴄᴏᴜɴᴛ ғᴏʀ ᴛʜᴇ ᴜsᴇʀ ᴀɴᴅ ɢᴇɴᴇʀᴀᴛᴇs ᴀ ᴜsᴇʀɴᴀᴍᴇ ᴀɴᴅ ᴘᴀssᴡᴏʀᴅ ғᴏʀ sᴛᴏʀɪɴɢ ᴍᴇᴅɪᴀs\n● /login - Aʟʟᴏᴡs ᴜsᴇʀs ᴛᴏ ʟᴏɢ ɪɴ ᴡɪᴛʜ ᴛʜᴇɪʀ ᴜsᴇʀ ID, ᴜsᴇʀɴᴀᴍᴇ, ᴀɴᴅ ᴘᴀssᴡᴏʀᴅ.\n● /show - Rᴇᴛʀɪᴇᴠᴇs ᴀɴᴅ ᴅɪsᴘʟᴀʏs ᴛʜᴇ ᴜsᴇʀ's ᴜsᴇʀɴᴀᴍᴇ ᴀɴᴅ ᴘᴀssᴡᴏʀᴅ.\n● /logout - Lᴏɢs ᴛʜᴇ ᴜsᴇʀ ᴏᴜᴛ ᴀɴᴅ ʀᴇᴍᴏᴠᴇs ᴛʜᴇɪʀ ʟᴏɢɪɴ sᴛᴀᴛᴜs.\n● /delete - Dᴇʟᴇᴛᴇs ᴛʜᴇ ᴜsᴇʀ's ᴀᴄᴄᴏᴜɴᴛ ᴀɴᴅ ᴀʟʟ ᴀssᴏᴄɪᴀᴛᴇᴅ ᴅᴀᴛᴀ." ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'up_pic':
        buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='helpp') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=f"ʜɪ {query.from_user.mention}\n\n● Fɪʀsᴛ sᴇɴᴅ ᴀ ᴘɪᴄ ғᴏʀ sᴀᴠɪɴɢ ɪɴ ᴏᴜʀ ᴅʙ.\n● /pics - ғᴏʀ ᴠɪᴇᴡ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴘʜᴏᴛᴏs ᴛʜᴀᴛ sᴛᴏʀᴇᴅ ɪɴ ᴏᴜʀ ᴅʙ.\n● /del_one - Rᴇᴘʟʏ ᴛᴏ ᴀ ᴏɴᴇ ᴘʜᴏᴛᴏ ғᴏʀ ᴅᴇʟᴇᴛᴇ ɪᴛ.\n" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'up_vid':
        buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='helpp') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=f"ʜɪ {query.from_user.mention}\n\n● Fɪʀsᴛ sᴇɴᴅ ᴀ ᴠɪᴅᴇᴏ ғᴏʀ sᴀᴠɪɴɢ ɪɴ ᴏᴜʀ ᴅʙ.\n● /vids - ғᴏʀ ᴠɪᴇᴡ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴠɪᴅᴇᴏ ᴛʜᴀᴛ sᴛᴏʀᴇᴅ ɪɴ ᴏᴜʀ ᴅʙ.\n● /del_one - Rᴇᴘʟʏ ᴛᴏ ᴀ ᴏɴᴇ ᴠɪᴅᴇᴏ ғᴏʀ ᴅᴇʟᴇᴛᴇ ɪᴛ.\n" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'up_aud':
        buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='helpp') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=f"ʜɪ {query.from_user.mention}\n\n● Fɪʀsᴛ sᴇɴᴅ ᴀ ᴀᴜᴅɪᴏ ғᴏʀ sᴀᴠɪɴɢ ɪɴ ᴏᴜʀ ᴅʙ.\n● /auds - ғᴏʀ ᴠɪᴇᴡ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴀᴜᴅɪᴏ ᴛʜᴀᴛ sᴛᴏʀᴇᴅ ɪɴ ᴏᴜʀ ᴅʙ.\n● /del_one - Rᴇᴘʟʏ ᴛᴏ ᴀ ᴏɴᴇ ᴀᴜᴅɪᴏ ғᴏʀ ᴅᴇʟᴇᴛᴇ ɪᴛ.\n" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'up_doc':
        buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='helpp') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=f"ʜɪ {query.from_user.mention}\n\n● Fɪʀsᴛ sᴇɴᴅ ᴀ ᴅᴏᴄᴜᴍᴇɴᴛ ғᴏʀ sᴀᴠɪɴɢ ɪɴ ᴏᴜʀ ᴅʙ.\n● /docs - ғᴏʀ ᴠɪᴇᴡ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴅᴏᴄᴜᴍᴇɴᴛ ᴛʜᴀᴛ sᴛᴏʀᴇᴅ ɪɴ ᴏᴜʀ ᴅʙ.\n● /del_one - Rᴇᴘʟʏ ᴛᴏ ᴀ ᴏɴᴇ ᴅᴏᴄᴜᴍᴇɴᴛ ғᴏʀ ᴅᴇʟᴇᴛᴇ ɪᴛ.\n" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'up_storage_del':
        buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='helpp') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=f"ʜɪ {query.from_user.mention}\n\n● /clear - Iᴛ ᴘʀᴇsᴇɴᴛs ᴏᴘᴛɪᴏɴs ᴛᴏ ᴅᴇʟᴇᴛᴇ sᴘᴇᴄɪғɪᴄ ᴍᴇᴅɪᴀ ᴛʏᴘᴇs  ʟɪᴋᴇ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏs, ᴅᴏᴄᴜᴍᴇɴᴛs ᴜsɪɴɢ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs..\n● /clear_all - ᴀsᴋ ғᴏʀ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ sᴛᴏʀᴇᴅ ᴍᴇᴅɪᴀ ᴘɪᴄs, ᴠɪᴅᴇᴏs, ᴀᴜᴅɪᴏ, ᴅᴏᴄᴜᴍᴇɴᴛs." ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'help':
        buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='start') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="Welcome to the photo saver bot.\n Here are the commands:\n\n● /help - for getting the tutorial video of how to use the bot\n\n● /create - For storing the pics to create a storage.\n\n● /login - Login for the access of ur pic to view and also delete.\n\n● /logout - it will logout the session.\n\n● /show - If you forget your username and password then send /show then the bot will send the username and password. (There is no need to login to use the /show).\n\n● /delete -  If you wanna to delete the created account in our bot, send /delete then it will delete all the datas stored in db.\n\n● /pics - List your saved photos\n\n● /del_one - Delete a specific photo, reply to the photo.\n\n● /del_many - Delete all your saved photos" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'about':
        user_id = query.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        if update_existing_db:
            buttons = [[
                InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='start') ,
                InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text="✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a href='https://t.me/MrTG_Coder'>ᴍʀ.ʙᴏᴛ ᴛɢ</a>\n✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>\n✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>\n✯ Mʏ Sᴇʀᴠᴇʀ: <a href='https://t.me/mrtgcoderbot'>ᴏʙᴀɴᴀɪ</a>\n✯ Pʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: ᴠ2.0.106\n✯ Mʏ ᴠᴇʀsɪᴏɴ: ᴠ5.0\n✯ ᴍʏ sᴇᴄᴜʀɪᴛʏ: ᴠ4.5" ,
                disable_web_page_preview=True , reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)
        elif not update_existing_db:
            buttons = [[
                InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='start') ,
                InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(text=ABOUT_TXT , disable_web_page_preview=True , reply_markup=reply_markup ,
                                          parse_mode=enums.ParseMode.HTML)

    elif query.data == 'clear_p_v_a_d':
      try:
        user_id = query.from_user.id
        confirmation_message = "Sᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴇᴅɪᴀ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴛʜᴇ sᴛᴏʀᴇᴅ ᴅᴀᴛᴀs"
        buttons = [[
            InlineKeyboardButton("ᴘɪᴄs" , callback_data="pics")
        ] , [
            InlineKeyboardButton("ᴠɪᴅᴇᴏs" , callback_data="videos")
        ] , [
            InlineKeyboardButton("ᴀᴜᴅɪᴏ" , callback_data="audios")
        ] , [
            InlineKeyboardButton("ᴅᴏᴄᴜᴍᴇɴᴛ" , callback_data="document")
        ] , [
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=confirmation_message ,
            reply_markup=reply_markup ,
            parse_mode=enums.ParseMode.HTML
        )
      except Exception as e:
        print(e)


    elif query.data == 'pics':
        try:
            user_id = query.from_user.id
            confirmation_message = "Aʀᴇ ʏᴏᴜ sᴜʀᴇ, ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴘɪᴄs ᴛʜᴀᴛ ʏᴏᴜ sᴛᴏʀᴇᴅ ɪɴ?\n\nIғ ʏᴏᴜ ᴄʟɪᴄᴋ ᴛʜᴇ ʏᴇs ʙᴜᴛᴛᴏɴ ɪᴛ ᴡɪʟʟ ᴇᴀʀsᴇ ᴀʟʟ ᴘɪᴄs.<b>ʏᴇs</b> ᴛᴏ ᴄᴏɴғɪʀᴍ ᴏʀ <b>ɴᴏ</b> ᴛᴏ ᴄᴀɴᴄᴇʟ."
            buttons = [[
                InlineKeyboardButton("ʏᴇs" , callback_data="pic_d_y")
            ] , [
                InlineKeyboardButton("ʜᴏᴍᴇ" , callback_data="clear_p_v_a_d") ,
                InlineKeyboardButton("ɴᴏ" , callback_data="close")
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=confirmation_message ,
                reply_markup=reply_markup ,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            print(e)


    elif query.data == 'pic_d_y':
        user_id = query.from_user.id
        collection.delete_many({"user_id": user_id})
        await client.send_message(user_id , text="ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴘɪᴄs ᴛʜᴀᴛ ʏᴏᴜ sᴛᴏʀᴇᴅ ɪɴ")

    elif query.data == 'videos':
        try:
            user_id = query.from_user.id
            confirmation_message = "Aʀᴇ ʏᴏᴜ sᴜʀᴇ, ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴠɪᴅᴇᴏs ᴛʜᴀᴛ ʏᴏᴜ sᴛᴏʀᴇᴅ ɪɴ?\n\nIғ ʏᴏᴜ ᴄʟɪᴄᴋ ᴛʜᴇ ʏᴇs ʙᴜᴛᴛᴏɴ ɪᴛ ᴡɪʟʟ ᴇᴀʀsᴇ ᴀʟʟ ᴠɪᴅᴇᴏs.<b>ʏᴇs</b> ᴛᴏ ᴄᴏɴғɪʀᴍ ᴏʀ <b>ɴᴏ</b> ᴛᴏ ᴄᴀɴᴄᴇʟ."
            buttons = [[
                InlineKeyboardButton("ʏᴇs" , callback_data="vid_d_y")
            ] , [
                InlineKeyboardButton("ʜᴏᴍᴇ" , callback_data="clear_p_v_a_d") ,
                InlineKeyboardButton("ɴᴏ" , callback_data="close")
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=confirmation_message ,
                reply_markup=reply_markup ,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            print(e)
    elif query.data == 'vid_d_y':
        user_id = query.from_user.id
        collection.delete_many({"v_user_id": user_id})
        await client.send_message(user_id , text="ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴠɪᴅᴇᴏs ᴛʜᴀᴛ ʏᴏᴜ sᴛᴏʀᴇᴅ ɪɴ")

    elif query.data == 'audios':
        user_id = query.from_user.id
        confirmation_message = "Aʀᴇ ʏᴏᴜ sᴜʀᴇ, ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴀᴜᴅɪᴏs ᴛʜᴀᴛ ʏᴏᴜ sᴛᴏʀᴇᴅ ɪɴ?\n\nIғ ʏᴏᴜ ᴄʟɪᴄᴋ ᴛʜᴇ ʏᴇs ʙᴜᴛᴛᴏɴ ɪᴛ ᴡɪʟʟ ᴇᴀʀsᴇ ᴀʟʟ ᴀᴜᴅɪᴏs.<b>ʏᴇs</b> ᴛᴏ ᴄᴏɴғɪʀᴍ ᴏʀ <b>ɴᴏ</b> ᴛᴏ ᴄᴀɴᴄᴇʟ."
        buttons = [[
            InlineKeyboardButton("ʏᴇs" , callback_data="aud_d_y")
        ] , [
            InlineKeyboardButton("ʜᴏᴍᴇ" , callback_data="clear_p_v_a_d") ,
            InlineKeyboardButton("ɴᴏ" , callback_data="close")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=confirmation_message ,
            reply_markup=reply_markup ,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == 'aud_d_y':
        user_id = query.from_user.id
        collection.delete_many({"a_user_id": user_id})
        await client.send_message(user_id , text="ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴀᴜᴅɪᴏ ᴛʜᴀᴛ ʏᴏᴜ sᴛᴏʀᴇᴅ ɪɴ")

    elif query.data == 'document':
        user_id = query.from_user.id
        confirmation_message = "Aʀᴇ ʏᴏᴜ sᴜʀᴇ, ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴅᴏᴄᴜᴍᴇɴᴛs ᴛʜᴀᴛ ʏᴏᴜ sᴛᴏʀᴇᴅ ɪɴ?\n\nIғ ʏᴏᴜ ᴄʟɪᴄᴋ ᴛʜᴇ ʏᴇs ʙᴜᴛᴛᴏɴ ɪᴛ ᴡɪʟʟ ᴇᴀʀsᴇ ᴀʟʟ ᴅᴏᴄᴜᴍᴇɴᴛs.<b>ʏᴇs</b> ᴛᴏ ᴄᴏɴғɪʀᴍ ᴏʀ <b>ɴᴏ</b> ᴛᴏ ᴄᴀɴᴄᴇʟ."
        buttons = [[
            InlineKeyboardButton("ʏᴇs" , callback_data="doc_d_y")
        ] , [
            InlineKeyboardButton("ʜᴏᴍᴇ" , callback_data="clear_p_v_a_d") ,
            InlineKeyboardButton("ɴᴏ" , callback_data="close")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=confirmation_message ,
            reply_markup=reply_markup ,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == 'doc_d_y':
        user_id = query.from_user.id
        collection.delete_many({"d_user_id": user_id})
        await client.send_message(user_id , text="ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴅᴏᴄᴜᴍᴇɴᴛ ᴛʜᴀᴛ ʏᴏᴜ sᴛᴏʀᴇᴅ ɪɴ")

    elif query.data == 'yup_data':
        user_id = query.from_user.id
        collection.delete_many({"user_id": user_id})
        collection.delete_many({"v_user_id": user_id})
        collection.delete_many({"a_user_id": user_id})
        collection.delete_many({"d_user_id": user_id})
        await client.send_message(user_id , text="sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ᴍᴇᴅɪᴀ")
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)

    elif query.data == 'nope_data':
        user_id = query.from_user.id
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)

    elif query.data == 'yess':
        user_id = query.from_user.id
        update_existing_db = collection.find_one({"update": user_id})
        if update_existing_db:
            collection.delete_one({"user_ids": user_id})
            collection.delete_many({"user_id": user_id})
            collection.delete_many({"v_user_id": user_id})
            collection.delete_many({"a_user_id": user_id})
            collection.delete_many({"d_user_id": user_id})
            collection.delete_one({"login": user_id})
            collection.delete_one({"update": user_id})
            await client.send_message(user_id , text="Yᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ..")
            await query.message.delete()
            edited_keyboard = InlineKeyboardMarkup([])
            await query.answer()
            await query.message.edit_reply_markup(edited_keyboard)
        elif not update_existing_db:
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
