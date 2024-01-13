from pyrogram import filters, Client

# Define the command handler for the '/delete' command
@Client.on_message(filters.command("delete"))
async def delete_messages(client, message):
    # Get the chat ID of the current chat
    chat_id = message.chat.id

    # Delete all messages in the current chat
    deleted_messages = await client.delete_messages(chat_id)

    # Send a confirmation message to the user
    await client.send_message(chat_id, "All messages in this chat have been deleted.")

