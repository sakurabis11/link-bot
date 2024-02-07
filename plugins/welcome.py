import pyrogram
from pyrogram import filters, Client, enums
import pymongo
from pyrogram.errors import *
from info import DATABASE_NAME, DATABASE_URI

# Connect to MongoDB
client = pymongo.MongoClient(DATABASE_URI)  
db = client[DATABASE_NAME]
collection = db["locks"]  

@Client.on_message(filters.command("set_welcome") & filters.group)
async def set_welcome(client, message):
 try:
  user = await client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
    raise PermissionError("You are not allowed to use this command")
    
  new_member = await message.chat.get_members(filters.chat_member_status.NEW_CHAT_MEMBERS)
  user_id = new_member[0].user.id
  user_info = await client.get_users(user_id)
  first_name = user_info.first_name
  last_name = user_info.last_name
  username = user_info.username
  mention = user_info.mention
  chat_name = message.chat.title
  chat_id = message.chat.id
  welcome_template = message.text.split(" ", 1)[1]
  welcome_code = generate_unique_code() 
  collection.insert_one({"chat_id": chat_id, "type": welcome_template, "code": welcome_code})
  await message.reply_text("Welcome message set successfully")
 except PermissionError as e:
  await message.reply_text(str(e))
 except Exception as e:
  await message.reply_text(str(e))

@Client.on_message(filters.command("see_welcome") & filters.group)
async def set_welcome(client, message):
 try:
  user = await client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
    raise PermissionError("You are not allowed to use this command")
  chat_id = message.chat.id
  welcome_message = collection.find_one({"chat_id": chat_id})["type"]
  await message.reply_text(f"welcome message: {welcome_message}")
 except PermissionError as e:
  await message.reply_text(str(e))
 except Exception as e:
  await message.reply_text(str(e))

@Client.on_message(filters.command("del_welcome") & filters.group)
async def set_welcome(client, message):
 try:
  user = await client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
    raise PermissionError("You are not allowed to use this command")
  chat_id = message.chat.id
  del_message = collection.delete_one({"chat_id": chat_id})
  if del_message.deleted_count == 0:
    await message.reply_text("welcome message is not set")
  else:
    await message.replly_text("welcome message suceesfully deleted")
 except PermissionError as e:
    await message.reply_text(str(e))
 except Exception as e:
    await message.reply_text(str(e))

@Client.on_message(filters.new_chat_members & filters.group)
async def welcome_new_user(client, message):
 try:
  chat_id = message.chat.id
  welcome_message = collection.find_one({"chat_id": chat_id})["type"]
  welcome_code = collection.find_one({"chat_id": chat_id})["code"]
  for new_member in message.new_chat_members:
    user_id = new_member.id
    user_info = await client.get_users(user_id)
    first_name = user_info.first_name
    last_name = user_info.last_name
    username = user_info.username
    mention = user_info.mention
    welcome_text = welcome_message.format(first_name=first_name, last_name=last_name, username=username, mention=mention, chat_name=message.chat.title, chat_id=message.chat.id, welcome_code=welcome_code)
    await message.reply_text(welcome_text)
 except Exception as e:
    await message.reply_text(str(e))
