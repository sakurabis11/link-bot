import pyrogram
from pyrogram import Client, filters
import os

CHANNEL_ID = -1002055184812

@Client.on_message(filters.private & filters.text)
async def forward_message(client, message):
    try:
        # Extract the requested user mention, if any
        user_mention = message.text.split(" ")[0] if message.text.startswith("@") else None

        # Forward the message with or without mention
        if user_mention:
            await client.forward_messages(
                chat_id=CHANNEL_ID,
                from_chat_id=message.chat.id,
                message_ids=message.message_id,
                # Include user mention using entities
                entities=[{"type": "text_mention", "offset": 0, "length": len(user_mention)}]
            )
        else:
            await client.forward_messages(
                chat_id=CHANNEL_ID,
                from_chat_id=message.chat.id,
                message_ids=message.message_id
            )
    except Exception as e:
        print(f"Error forwarding message: {e}")
