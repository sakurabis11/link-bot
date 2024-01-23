from pyrogram import Client, filters, enums
from pyrogram.types import Message
from database.users_db import db

@Client.on_message(filters.command("set_welcome"))
async def set_welcome(client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        return await message.reply_text("You are not allowed to use this command")
    if len(message.command) == 1:
        return await message.reply_text("Please provide a welcome message")
    welcome_message = message.text.split(" ", 1)[1]
    await db.set_welcome(message.chat.id, welcome_message=welcome_message)
    await message.reply_text(f"Welcome message successfully set for this chat")  

@Client.on_message(filters.command("welcome_message_remove"))
async def remove_welcome(client, message: Message):  # Function name corrected
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        return await message.reply_text("You are not allowed to use this command")
    welcome_message = await db.get_welcome(message.chat.id)  # Retrieve welcome message
    if not welcome_message:
        return await message.reply_text(f"There's no welcome message set for this chat")
    await db.set_welcome(message.chat.id, welcome_message=None)
    await message.reply_text(f"Welcome message successfully removed from this chat")
