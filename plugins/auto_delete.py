import pyrogram
from pyrogram import Client, filters

@Client.on_message(filters.command("clearall"))
async def clear_messages(client, message):
    chat_id = message.chat.id

    if message.chat.type == "group" or message.chat.type == "supergroup":
        await client.delete_messages(chat_id, message.chat.all_messages())
        await message.reply_text("All messages deleted in the group!")
    elif message.chat.type == "channel":
        await client.delete_messages(chat_id, message.chat.history())
        await message.reply_text("All messages deleted in the channel!")
    else:
        await message.reply_text("This command can only be used in groups and channels.")
