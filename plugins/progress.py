import asyncio
from pyrogram import Client, filters

async def send_progress_bar(chat_id, progress, message="Progress:", comment=""):
    message = await app.send_message(chat_id, message + f" {progress}%")
    await message.edit(message + f" {progress}% ({comment})")  

@Client.on_message(filters.command("progress"))
async def start_handler(client, message):
    await message.reply("Starting process...")

    for i in range(1, 11):
        await asyncio.sleep(1)  # Simulate a task taking time
        await send_progress_bar(message.chat.id, i * 10, comment=f"Step {i}")

    await message.reply("Update done!")

