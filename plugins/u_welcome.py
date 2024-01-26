from pyrogram import Client, filters, enums
from database.users_db import db
from pyrogram.errors import *

@Client.on_message(filters.command("set_welcome") & filters.group)
async def set_welcome(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        raise PermissionError("You are not allowed to use this command")  
    query = message.text.split(" ", 1)[1]
    await message.reply_text("Welcome message set!")
    db.save_welcome_message(message.chat.id, query)

@Client.on_message(filters.command("view_welcome") & filters.group)
async def view_welcome(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        raise PermissionError("You are not allowed to use this command")  
    message = db.get_welcome_message(message.chat.id)
    if message:
        await message.reply_text("Current welcome message:\n" + message)
    else:
        await message.reply_text("No welcome message set for this group.")

@Client.on_message(filters.command("del_welcome") & filters.group)
async def del_welcome(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        raise PermissionError("You are not allowed to use this command")  
    db.delete_welcome_message(message.chat.id)
    await message.reply_text("Welcome message deleted!")

@Client.on_message(filters.group & filters.new_chat_members)
async def welcome_new_member(client, message):
    for new_member in message.new_chat_members:
        welcome_message = db.get_welcome_message(message.chat.id)
        if welcome_message:
            try:
                await message.reply_text(welcome_message.format(mention=new_member.mention))
            except Exception as e:
                print(f"Error sending welcome message: {e}")


