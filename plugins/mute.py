import pyrogram
from pyrogram import filters, Client
from datetime import timedelta

@Client.on_message(filters.command("mute") & filters.incoming)
async def mute_user(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
    if await message.chat.get_member(message.from_user.id).can_restrict_members and await client.get_chat_member(message.chat.id, message.from_user.id).can_restrict_members:
        try:
            reply_message = message.reply_to_message
            if reply_message:
                user_to_mute = reply_message.from_user

                # Parse the mute duration from the command
                command_args = message.command[1].split()
                try:
                    days = int(command_args[0])
                    minutes = int(command_args[1])
                    seconds = int(command_args[2])
                except (IndexError, ValueError):
                    await message.reply_text("Invalid mute duration format. Please specify days, minutes, and seconds.")
                    return

                mute_until = datetime.now() + timedelta(days=days, minutes=minutes, seconds=seconds)

                # Restrict the user with appropriate permissions
                await message.chat.restrict_member(
                    user_to_mute.id,
                    can_send_messages=False,
                    until_date=mute_until
                )

                await message.reply_text(f"{user_to_mute.mention} has been muted for {days} days, {minutes} minutes, and {seconds} seconds.")
        except Exception as e:
            await message.reply_text(f"An error occurred: {e}")
    else:
        await message.reply_text("You are not authorized to use this command.")

app.run()
