from pyrogram import Client, filters
from info import ADMINS
import os

admin_id = ADMINS
forward_channel_id = "-1002029706461"

@Client.on_message(filters.private & ~filters.forwarded)
async def forward_to_admin(client, message):
    # Forward the message to the admin chat
    client.forward_messages(chat_id=admin_id, from_chat_id=message.chat.id, message_ids=message.message_id)

@Client.on_message(filters.chat(forward_channel_id) & filters.private)
async def forward_to_channel(client, message):
    # Forward the message to the specified channel
    client.forward_messages(chat_id=forward_channel_id, from_chat_id=message.chat.id, message_ids=message.message_id)

