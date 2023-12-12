from pyrogram import Client, filters
from datetime import date, datetime, timezone

# Define the welcome message template
welcome_message_template = """\
 Hey {u.mention}, welcome to {message.chat.title}! 

{today} at {time}
"""

# Define a dictionary to store group IDs and their respective welcome messages
welcome_messages = {}

@Client.on_message(filters.command("set_welcome") & filters.group)
async def set_welcome(client, message):
    """
    Handle the "/set_welcome" command for group owners/admins.
    """
    if not message.chat.sender_chat:
        return await message.reply("This command can only be used in groups.")
    
    if not message.chat.sender_chat.has_rights("administrator"):
        return await message.reply("You need administrator privileges to use this command.")

    # Get the welcome message from the message content
    welcome_message = message.text.split(" ", 1)[1]

    # Update the welcome message for the current group
    welcome_messages[message.chat.id] = welcome_message

    await message.reply("Welcome message set successfully!")

@Client.on_message(filters.group & filters.new_chat_members)
async def welcome_new_members(client, message):
    """
    Welcome new members to the group.
    """
    # Check if the group has a custom welcome message
    if message.chat.id not in welcome_messages:
        return

    # Format the welcome message with data
    welcome_message = welcome_message_template.format(
        u=message.new_chat_members[0],
        message=message,
        today=date.today().strftime("%d/%m/%Y"),
        time=datetime.now(timezone.utc).strftime("%H:%M:%S %p"),
    )

    await message.reply(welcome_message)

