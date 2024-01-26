import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import *
import pymongo
from info import DATABASE_URI

MONGO_URI = DATABASE_URI

db = pymongo.MongoClient(MONGO_URI)["welcome_bot"]

@Client.on_message(filters.command(["set_welcome"]) & filters.group)
async def set_welcome(client, message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            raise PermissionError("You are not allowed to use this command")
          
        query = message.text.split(" ", 1)[1] 
        await db.welcome_messages.update_one({"chat_id": message.chat.id}, {"$set": {"message": query}}, upsert=True)
        await message.reply_text("Welcome message set successfully!")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command(["view_welcome"]) & filters.group)
async def view_welcome(client, message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            raise PermissionError("You are not allowed to use this command")
          
        welcome_message = await db.welcome_messages.find_one({"chat_id": message.chat.id})
        if welcome_message:
            await message.reply_text(f"Current welcome message:\n{welcome_message['message']}")
        else:
            await message.reply_text("No welcome message set for this group.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command(["del_welcome"]) & filters.group)
async def del_welcome(client, message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            raise PermissionError("You are not allowed to use this command")
          
        await db.welcome_messages.delete_one({"chat_id": message.chat.id})
        await message.reply_text("Welcome message deleted successfully!")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.group & filters.new_chat_members)
async def welcome_new_members(client, message):
    welcome_message = await db.welcome_messages.find_one({"chat_id": message.chat.id})
    if welcome_message:
        for new_member in message.new_chat_members:
            await message.reply_text(welcome_message["message"].format(mention=new_member.mention))

