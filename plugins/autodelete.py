from pyrogram import Client, filters
from datetime import datetime, timedelta

# Define a dictionary to store deletion times for each chat
chat_deletion_times = {}

@Client.on_message(filters.command("set_time") & filters.chat_admins)
async def set_delete_time(client, message):
    global chat_deletion_times

    if not message.reply_to_message:
        await message.reply_text("Please reply to a message in the chat you want to set the auto-delete time for.")
        return

    chat_id = message.chat.id

    try:
        # Extract time and unit
        time_value, time_unit = message.text.split()[1:3]
        time_value = int(time_value)
    except ValueError:
        await message.reply_text("Invalid time format. Please specify the time and unit (e.g., 5 minutes, 3 hours).")
        return

    # Convert time to timedelta based on unit
    if time_unit == "seconds":
        delete_time = timedelta(seconds=time_value)
    elif time_unit == "minutes":
        delete_time = timedelta(minutes=time_value)
    elif time_unit == "hours":
        delete_time = timedelta(hours=time_value)
    elif time_unit == "days":
        delete_time = timedelta(days=time_value)
    elif time_unit == "months":
        delete_time = timedelta(days=time_value * 30)  # Approximate months as 30 days
    else:
        await message.reply_text(f"Invalid time unit. Supported units are seconds, minutes, hours, days, and months.")
        return

    chat_deletion_times[chat_id] = datetime.utcnow() + delete_time
    await message.reply_text(f"Auto-delete time set to {time_value} {time_unit} for this chat.")

@Client.on_message(filters.group | filters.channel | filters.supergroup)
async def check_for_deletion(client, message):
    global chat_deletion_times

    chat_id = message.chat.id
    if chat_id not in chat_deletion_times:
        return

    if datetime.utcnow() > chat_deletion_times[chat_id]:
        await message.delete()
        del chat_deletion_times[chat_id]

