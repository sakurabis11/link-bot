from pyrogram import Client, filters
from datetime import timedelta

# Function to check if user is owner or admin
async def is_owner_or_admin(client, message):
  chat_members = await client.get_chat_members(message.chat.id)
  for member in chat_members:
    if member.status in ("creator", "administrator"):
      if member.user.id == message.from_user.id:
        return True
  return False

# Function to delete all messages in a chat
async def delete_all_messages(chat_id, time_delta):
  # Get chat information
  chat = await app.get_chat(chat_id)

  # Check if the chat is a group or channel
  if chat.type not in ("group", "supergroup", "channel"):
    return

  # Get all messages in the chat
  messages = await app.get_chat_history(chat_id)

  # Check if the user is owner or admin
  if not await is_owner_or_admin(client, message):
    await message.reply_text("Only group and channel owners or admins can use this command.")
    return

  # Check if auto-delete is enabled
  global auto_delete_enabled
  if auto_delete_enabled:
    # Delete messages in batches
    for message in messages:
      await app.delete_messages(chat_id, message.message_id)

    # Wait for the specified time
    await asyncio.sleep(time_delta.total_seconds())

# Global variable to track auto-deletion status
auto_delete_enabled = True

# Command handler for setting the time
@Client.on_message(filters.command(["set_time"]))
async def set_time(client, message):
  # Check if user is owner or admin
  if not await is_owner_or_admin(app, message):
    await message.reply_text("Only group and channel owners or admins can use this command.")
    return

  # Check if arguments are provided
  if len(message.command) < 2:
    await message.reply_text("Please provide the time in seconds, minutes, hours, or days.")
    return

  time_str = message.command[1]

  # Parse the time string
  try:
    time_delta = parse_time(time_str)
  except ValueError:
    await message.reply_text("Invalid time format.")
    return

  await message.reply_text(f"Time set to {time_delta}")

@Client.on_message(filters.command(["delete_all"]))
async def delete_all(client, message):
  # Check if user is owner or admin
  if not await is_owner_or_admin(app, message):
    await message.reply_text("Only group and channel owners or admins can use this command.")
    return

  # Check if the chat is a group or channel
  if message.chat.type not in ("group", "supergroup", "channel"):
    await message.reply_text("This command is only available in groups and channels.")
    return

  # Delete messages in the chat
  await delete_all_messages(message.chat.id, time_delta)

  await message.reply_text("Deleted all messages.")

@Client.on_message(filters.command(["autodelete_off"]))
async def autodelete_off(client, message):
  # Check if user is owner or admin
  if not await is_owner_or_admin(app, message):
    await message.reply_text("Only group and channel owners or admins can use this command.")
    return

  # Disable auto-deletion
  global auto_delete_enabled
  auto_delete_enabled = False

  await message.reply_text("Auto-deletion is now disabled.")

# Function to parse the time string
def parse_time(time_str):
  if time_str.endswith("s"):
    return timedelta(seconds=int(time_str[:-1]))
  elif time_str.endswith("m"):
    return timedelta(minutes=int(time_str[:-1]))
  elif time_str.endswith("h"):
    return timedelta(hours=int(time_str[:-1]))
  elif time_str.endswith("d"):
    return timedelta(days=int(time_str[:-1]))
  
