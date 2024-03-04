import asyncio
from pyrogram import Client, filters
from pymongo import MongoClient
from info import DATABASE_NAME, DATABASE_URI

mongo_client = MongoClient(DATABASE_URI)
db = mongo_client[DATABASE_NAME] 
collection = db["welcome_messages"]  

async def set_welcome(client, message):
    chat_id = message.chat.id
    new_welcome_text = message.text.split(maxsplit=1)[1].strip()  

    await collection.update_one(
        {"chat_id": chat_id}, {"$set": {"welcome_text": new_welcome_text}}, upsert=True
    )
    await message.reply_text(f"Welcome message set to: {new_welcome_text}")

async def view_welcome(client, message):
    chat_id = message.chat.id
    welcome_message = await collection.find_one({"chat_id": chat_id})

    if welcome_message:
        await message.reply_text(welcome_message["welcome_text"])
    else:
        await message.reply_text("No welcome message set for this group.")

async def delete_welcome(client, message):
    chat_id = message.chat.id
    delete_result = await collection.delete_one({"chat_id": chat_id})

    if delete_result.deleted_count > 0:
        await message.reply_text("Welcome message deleted successfully.")
    else:
        await message.reply_text("No welcome message found for this group.")

async def welcome_new_member(client, event):
    new_members = event.new_chat_members
    chat_id = event.chat.id

    welcome_message = await collection.find_one({"chat_id": chat_id})

    if welcome_message:
        welcome_text = welcome_message["welcome_text"]
        for member in new_members:
            user_mention = f"[{(member.username or member.first_name)}](tg://user?id={member.id})"
            await client.send_message(chat_id, f"{welcome_text} {user_mention}")

@CLient.on_message(filters.command("set_welcome") & filters.group)
async def set_welcome_handler(client, message):
    await set_welcome(client, message)

@Client.on_message(filters.command("view_welcome") & filters.group)
async def view_welcome_handler(client, message):
    await view_welcome(client, message)

@CLient.on_message(filters.command("del_welcome") & filters.group)
async def delete_welcome_handler(client, message):
    await delete_welcome(client, message)

@Client.on_event(filters.new_chat_members)
async def welcome_new_member_handler(client, event):
    await welcome_new_member(client, event)


