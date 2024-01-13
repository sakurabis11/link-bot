
from pyrogram import filters, Client

@Client.on_message(filters.command("delete"))
async def delete_messages(client, message):
    user = message.from_user.id
    chat_id = message.chat.id
    group = await client.get_chat_members(chat_id)

    if user not in [member.user.id for member in group if member.status in ["creator", "administrator"]]:
        await message.reply_text("you are not allowed to use this command")
        return

    await message.reply_text("deleting all messages...")
    await client.delete_messages(chat_id, message_ids=range(1, message.message_id))
    await message.reply_text("all messages deleted")
