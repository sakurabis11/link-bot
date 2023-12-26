import pyrogram
from pyrogram import Client, filters

DELETE_COMMAND = "/delete"

@Client.on_message(filters.command(DELETE_COMMAND))
async def delete_messages(client, message):
    chat_id = message.chat.id
    user = message.from_user

    if message.chat.type == "group" or message.chat.type == "supergroup":
        is_admin = await client.get_chat_member(chat_id, user.id)
        is_admin = is_admin.status in ["administrator", "creator"]
    elif message.chat.type == "channel":
        is_admin = await client.get_chat_member(chat_id, user.id)
        is_admin = is_admin.status in ["creator", "administrator"]
    else:
        await message.reply_text("This command can only be used in groups or channels.")
        return

    if is_admin:
        try:
            await client.delete_messages(chat_id, range(1))
            await message.reply_text("All messages have been deleted.")
        except Exception as e:
            await message.reply_text("Failed to delete messages. Error: " + str(e))
    else:
        await message.reply_text("You are not allowed to send this command.")
