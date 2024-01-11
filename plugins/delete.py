import asyncio
from pyrogram import Client, filters, app  # Import app

@Client.on_message(filters.command("all_delete") & filters.group)
async def delete_all_messages(client, message):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = client.get_chat_member(chat_id, user_id)
    if not user_info.status == "administrator":
        await message.reply_text("You need to be an admin to use this command.")
        return

    # Check if the bot is an admin
    bot_info = client.get_chat_member(chat_id, client.get_me().id)  
    if not bot_info.status == "administrator":
        await message.reply_text("Please make sure the bot is an admin.")
        return

    # Delete messages efficiently
    messages = client.get_chat_history(chat_id)
    message_ids = [msg.message_id for msg in messages]
    await client.delete_messages(chat_id, message_ids)

    await message.reply_text("All messages deleted successfully.")





