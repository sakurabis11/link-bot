import pyrogram
from pyrogram import Client, filters, enum
from info import API_ID, API_HASH, BOT_TOKEN, PORT


new_users = 0
new_groups = 0

@Client.on_message()
async def handle_message(client, message):
    # Check if new users have been added
    if message.new_chat_members:
        global new_users
        new_users += len(message.new_chat_members)

    # Check if the message is from a supergroup (group)
    if message.chat.type == "supergroup":
        global new_groups
        new_groups += 1

    # Handle '/stats' command
    if message.text == "/stats":
        users = new_users
        groups = new_groups

        await message.reply(f"New users: {users}\nNew groups: {groups}")

@Client.on_idle()
async def idle():
    while True:
        # Send statistics message every 60 seconds
        await asyncio.sleep(60)

        # Fetch statistics
        users = new_users
        groups = new_groups

        # Reset counters
        new_users = 0
        new_groups = 0

        # Send statistics message
        await client.send_message("-1002084798134", f"New users: {users}\nNew groups: {groups}")
