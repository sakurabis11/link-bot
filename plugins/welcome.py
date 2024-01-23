from pyrogram import Client, filters, enums
from pyrogram.types import Message
from database.welcome_db import set_welcome, remove_welcome
from info import DATABASE_NAME, DATABASE_URI

@Client.on_message(filters.command("set_welcome"))
async def set_welcome(client, message: Message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            raise PermissionError("You are not allowed to use this command")

        if len(message.command) == 1:
            raise ValueError("Please provide a welcome message")

        welcome_message = message.text.split(" ", 1)[1]
        await set_welcome(message.chat.id)
        await message.reply_text(f"Welcome message successfully set for this chat")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command("welcome_message_remove"))
async def remove_welcome(client, message: Message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            raise PermissionError("You are not allowed to use this command")

        welcome_message = await db.get_welcome(message.chat.id)
        if not welcome_message:
            raise ValueError(f"There's no welcome message set for this chat")

        await set_welcome(message.chat.id, welcome_message=None)
        await message.reply_text(f"Welcome message successfully removed from this chat")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
