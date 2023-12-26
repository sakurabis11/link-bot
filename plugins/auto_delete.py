import pyrogram
from pyrogram import Client, filters

@Client.on_message(filters.command("clear") & (filters.chat_type.supergroup | filters.chat_type.channel) & filters.me)
async def handle_clear_command(client, message):
    try:
        chat_id = message.chat.id
        await client.delete_messages(chat_id, message.message_id)

        await client.send_message(chat_id, "Deleting all messages...")

        async for msg in client.iter_history(chat_id, limit=None):
            try:
                await client.delete_messages(chat_id, msg.message_id)
            except Exception as e:
                print(f"Error deleting message {msg.message_id}: {e}")

        await app.send_message(chat_id, "All messages deleted successfully!")
    except Exception as e:
        print(f"Error: {e}")
        await client.send_message(chat_id, "Failed to delete messages. Please check permissions.")


