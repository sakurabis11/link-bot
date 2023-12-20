import pyrogram
from pyrogram import Client, filters
import os

admin_channel_id = -1002079640571

@Client.on_message(filters.chat(~admin_channel_id) & (filters.text | filters.command | filters.forwarded))
async def forward_message_with_tag(client, message):
    if message.forward_from:
        # Forwarded message with tag
        await client.send_message(
            admin_channel_id,
            f"#forwarded\n{message.text}\n\nFrom: {message.forward_from.mention}",
            disable_web_page_preview=True  # Prevent potential privacy leaks
        )
    else:
        # Text message or command
        await client.send_message(
            admin_channel_id,
            f"#message\n{message.text}\n\nFrom: {message.from_user.mention}",
            disable_web_page_preview=True
        )
