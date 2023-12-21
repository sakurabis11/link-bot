import pyrogram
from pyrogram import Client, Filters



@Client.on_message(filters.chat(~admin_channel_id) & (filters.text | filters.command | filters.forwarded))
async def forward_message_with_tag(client, message):
    if message.forward_from:
        # Forwarded message with tag
        await client.send_message(
            admin_channel_id,
            f"#Forwarded\n{message.text}\nFrom: @{message.forward_from.username}",
            reply_to_message_id=message.message_id,
        )
    else:
        # User message or command with tag
        await client.send_message(
            admin_channel_id,
            f"#Message\n{message.text}\nFrom: @{message.from_user.username}",
            reply_to_message_id=message.message_id,
        )

