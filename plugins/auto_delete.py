import os
import asyncio
from info import DATABASE_URI
from pyrogram import Client, filters
from pymongo import MongoClient

MONGO_URI = DATABASE_URI

mongo = MongoClient(MONGO_URI)
db = mongo["auto_delete_bot"]
collection = db["chat_settings"]

@Client.on_message(filters.command("auto_delete") & (filters.chat_type.groups | filters.chat_type.channels))
async def handle_auto_delete(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check admin or owner status, adjusting for channel permissions
    if not (await client.get_chat_member(chat_id, user_id).can_manage_chat or
            await client.get_chat_member(chat_id, user_id).status in ["creator", "administrator"]):
        await message.reply_text("You are not allowed to manage this setting.")
        return

    command = message.command[1].lower()

    if command == "on":
        collection.update_one({"chat_id": chat_id}, {"$set": {"auto_delete_enabled": True}}, upsert=True)
        await message.reply_text("Auto-delete enabled.")
    elif command == "off":
        collection.update_one({"chat_id": chat_id}, {"$set": {"auto_delete_enabled": False}})
        await message.reply_text("Auto-delete disabled.")
    else:
        await message.reply_text("Invalid command. Use /auto_delete on or /auto_delete off")

async def delete_all_messages(chat_id):
    try:
        await app.delete_messages(chat_id, range(1))
    except Exception as e:
        print(f"Error deleting messages in chat {chat_id}: {e}")

@Client.on_message(filters.chat(chat_id=collection.find({"auto_delete_enabled": True})))
async def auto_delete(client, message):
    await asyncio.sleep(5)  # Delay before deletion
    await delete_all_messages(message.chat.id)

