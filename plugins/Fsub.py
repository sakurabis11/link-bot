from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

CHANNEL_1_ID = "-1001988807841"
CHANNEL_2_ID = "-1002076839389"

@Client.on_message(filters.command(""))
async def handle_command(client, message):
    # Get user ID and chat ID
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if user is member of both channels
    is_member_1 = await client.get_chat_member(CHANNEL_1_ID, user_id)
    is_member_2 = await client.get_chat_member(CHANNEL_2_ID, user_id)

    if not is_member_1 and not is_member_2:
        # Send join message for both channels
        join_message = f"Please join our channels for full access!\n\nChannel 1: {await client.export_chat_invite_link(CHANNEL_1_ID)}\nChannel 2: {await client.export_chat_invite_link(CHANNEL_2_ID)}"
        await message.reply(join_message)
    elif not is_member_1:
        # Send join message for channel 1
        join_message = f"Please join our other channel for full access!\n\nChannel 1: {await client.export_chat_invite_link(CHANNEL_1_ID)}"
        await message.reply(join_message)
    elif not is_member_2:
        # Send join message for channel 2
        join_message = f"Please join our other channel for full access!\n\nChannel 2: {await client.export_chat_invite_link(CHANNEL_2_ID)}"
        await message.reply(join_message)
    else:
        await message.reply_text("Now you can use this bot") 
