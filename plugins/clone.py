import pyrogram
from pyrogram import Client, filters

@Client.on_message(filters.command("clone") & filters.private)
async def clone_bot(client, message):
    bot_token = message.text.split()[1]  # Extract the bot token from the message

    try:
        # Create a new bot client for the cloned bot
        cloned_bot = Client(f"cloned_bot_{len(cloned_bots)}", bot_token=bot_token)
        await cloned_bot.start()

        await message.reply_text("Cloning...")

        # Add the cloned bot to the list
        cloned_bots.append(cloned_bot)

    except Exception as e:
        await message.reply_text(f"Error cloning bot: {e}")

@Client.on_message(filters.command("users") & filters.private)
async def count_users(client, message):
    total_users = 1  # Count the main bot as a user
    for cloned_bot in cloned_bots:
        total_users += await cloned_bot.get_me().total_count

    await message.reply_text(f"Total users: {total_users}")

