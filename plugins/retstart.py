import asyncio
from datetime import datetime
import time
from info import ADMINS
from pyrogram import Client, filters, emoji

PROGRESS_BAR_SYMBOLS = ['-', '\\', '|', '/']

restart_in_progress = False

@client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_handler(client, message):
    global restart_in_progress

    if restart_in_progress:
        await message.reply_text("Restart already in progress. Please wait.")
        return

    restart_in_progress = True

    try:
        restart_message = await message.reply_text(
            f"Restarting... {PROGRESS_BAR_SYMBOLS[0]}", reply_markup=filters.ReplyKeyboardMarkup([[filters.KeyboardButton("Cancel")]])
        )


        for i in range(10):
            time.sleep(0.5)
            new_symbol = PROGRESS_BAR_SYMBOLS[(i + 1) % len(PROGRESS_BAR_SYMBOLS)]
            await restart_message.edit(f"Restarting... {new_symbol}")

 
        await client.stop() 
        time.sleep(1)  
        print("Bot restarted successfully!")

        new_client = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
        await new_client.start()

        await restart_message.edit(
            f"Restarted successfully! {emoji.ROBOT}", reply_markup=filters.ReplyKeyboardRemove()
        )

    except asyncio.CancelledError:
        await restart_message.edit("Restart cancelled.", reply_markup=filters.ReplyKeyboardRemove())

    finally:
        restart_in_progress = False


