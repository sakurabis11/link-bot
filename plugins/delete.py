import logging
from pyrogram import Client, filters

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command("delete"))
async def handle_delete_command(client, message):
 try:
    if not message.chat.permissions.can_delete_messages:
        client.send_message(message.chat.id, "I don't have permission to delete messages in this chat.")
        return
    await message.delete()
 except Exception as e:
    await message.reply_text(f"{e}")
