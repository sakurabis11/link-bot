import pyrogram
from pyrogram import Client, filters
from info import ADMIN_CHANNEL_ID

@Client.on_message(filters.private & filters.chat)
async def forward_private_messages(client, message):
    # Construct the forwarded message with tag and user mention
    forwarded_message = f"#ForwardedMessage\n{message.from_user.mention}\n{message.text}"

    # Forward the message to the admin channel, keeping original formatting
    await client.forward_messages(
        ADMIN_CHANNEL_ID,
        message.chat.id,
        message_ids=message.message_id,
        as_copy=True  # Preserve original formatting
    )
