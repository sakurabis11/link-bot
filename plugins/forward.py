import pyrogram
from pyrogram import Client, filters
from info jmport ADMINS

# Replace with the chat IDs of the source and destination channels/groups
SOURCE_CHAT_ID = -1001234567890  # Example source channel ID
DESTINATION_CHAT_ID = -1111222233334444  # Example destination channel ID

@Client.on_message(filters.chat(SOURCE_CHAT_ID) & filters.command("forward") & filters.user(ADMINS))
async def forward_command(client, message):
    reply_message = message.reply_to_message

    if reply_message and reply_message.document or reply_message.video or reply_message.audio:
        try:
            await reply_message.copy(chat_id=DESTINATION_CHAT_ID)
            await message.reply_text("Forwarded successfully!")
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")  # Log errors for debugging
            await message.reply_text("Error forwarding message. Please check logs for details.")
    else:
        await message.reply_text("Please reply to a media message (file, document, video, or audio) to forward.")


