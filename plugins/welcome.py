import pyrogram
from pyrogram import Client, filters
from pymongo import MongoClient
import os
from info import DATABASE_NAME, DATABASE_URI

# MongoDB connection
mongo_client = MongoClient(os.getenv(DATABASE_URI))
db = mongo_client[DATABASE_NAME]
welcome_messages = db["welcome_messages"]

@Client.on_message(filters.command("w_help"))
async def help(client, message):
    await message.reply_text("Available commands:\n/set_welcome {welcome_message}\n/view_message\n/del_message")

@Client.on_message(filters.command("set_welcome") & filters.group)
async def set_welcome(client, message):
 try:
    welcome_message = message.text.split(" ", 1)[1]  
    chat_id = message.chat.id

    welcome_messages.update_one({"chat_id": chat_id}, {"$set": {"message": welcome_message}}, upsert=True)
    await client.send_message(chat_id=chat_id, text="Welcome message set successfully!")
 Exception as e:
    await message.reply_text(f"{e}")

@Client.on_message(filters.command("view_message"))
async def view_message(client, message):
 try:
    chat_id = message.chat.id
    stored_message = welcome_messages.find_one({"chat_id": chat_id})

    if stored_message:
        await client.send_message(chat_id=chat_id, text=stored_message["message"])
    else:
        await client.send_message(chat_id=chat_id, text="No welcome message set for this chat.")
 Exception as e:
    await message.reply_text(f"{e}")

@Client.on_message(filters.command("del_message"))
async def del_message(client, message):
 try:    
    chat_id = message.chat.id
    welcome_messages.delete_one({"chat_id": chat_id})
    await client.send_message(chat_id=chat_id, text="Welcome message deleted successfully!")
 Exception as e:
    await message.reply_text(f"{e}")

@Client.on_message(filters.new_chat_members)
async def welcome(client, message):
 try:
    stored_message = welcome_messages.find_one({"chat_id": message.chat.id})

    if stored_message:
        for user in message.new_chat_members:
            mention_format = f"<a href='tg://user?id={user.id}'>{user.full_name} ({user.id})</a>"
            welcome_text = stored_message["message"].format(mention_format=mention_format,
                                                           group_name=message.chat.title)
            await client.send_message(chat_id=message.chat.id, text=welcome_text)
 Exception as e:
    await message.reply_text(f"{e}")            

