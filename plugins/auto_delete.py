import pyrogram
from pyrogram import Client, filters


@Client.on_message(filters.command(["deleteall"], prefixes="!"))
async def delete_all_messages(client, message):
    chat_id = message.chat.id
    user = await app.get_chat_member(chat_id, message.from_user.id)

    if user.status in ["creator", "administrator"]:
        try:
            await client.delete_messages(chat_id, message.message_id - 1)
            await message.reply_text("All messages deleted successfully!")
        except Exception as e:
            await message.reply_text("Failed to delete messages. Error: " + str(e))
    else:
        await message.reply_text("You are not allowed to use this command.")

