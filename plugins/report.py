from pyrogram import Client, filters
CMD = '@'

@Client.on_message(filters.reply & filters.command("admins",CMD))
async def report_to_admins(client, message):
    # Get the replied message
    replied_message = message.reply_to_message

    # Check if the replied message exists
    if not replied_message:
        await message.reply("Please reply to a message you want to report.")
        return

    # Get the chat members list
    chat_members = await client.get_chat_members(message.chat.id)

    # Filter admins and owners
    admins = [member for member in chat_members if member.status in ("administrator", "creator")]

    # Send the report to each admin
    for admin in admins:
        await client.send_message(admin.user.id, f"**New report from {message.from_user.mention} in group {message.chat.title}**:\n\n{replied_message.text}")

    # Send confirmation message to the user
    await message.reply("Your report has been sent to the admins.")

