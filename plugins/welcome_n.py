
import asyncio
from pyrogram import Client, filters
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client.welcome_bot

@Client.on_message(filters.command("set_welcome"))
async def set_welcome(client, message):
    try:
        welcome_message = message.text.split(" ", maxsplit=1)[1]
        db.welcome_messages.update_one({"chat_id": message.chat.id}, {"$set": {"welcome_message": welcome_message}}, upsert=True)
        await message.reply_text("Welcome message set successfully!")
    except IndexError:
        await message.reply_text("Usage: /set_welcome ")

@Client.on_message(filters.command("view_welcome"))
async def view_welcome(client, message):
    welcome_message = db.welcome_messages.find_one({"chat_id": message.chat.id})
    if welcome_message:
        await message.reply_text(welcome_message["welcome_message"])
    else:
        await message.reply_text("No welcome message set for this chat.")

@Client.on_message(filters.command("delete_welcome"))
async def delete_welcome(client, message):
    db.welcome_messages.delete_one({"chat_id": message.chat.id})
    await message.reply_text("Welcome message deleted successfully!")

@Client.on_message(filters.new_chat_members)
async def send_welcome(client, message):
    welcome_message = db.welcome_messages.find_one({"chat_id": message.chat.id})
    if welcome_message:
        await client.send_message(message.chat.id, welcome_message["welcome_message"])


