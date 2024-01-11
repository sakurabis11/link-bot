import asyncio
from pyrogram import Client, filters

@Client.on_message(filters.command("all_delete") & filters.group)
async def delete_all_messages(client, message):
    chat_id = message.chat.id

    try:
        me = await client.get_me()
        await client.get_chat_member(chat_id, me.id)  

        async for message in client.iter_history(chat_id, limit=None):
            try:
                await client.delete_messages(chat_id, message.message_id)
            except Exception as e:
                print(f"Error deleting message: {e}")

        await message.reply_text("All messages have been deleted successfully!")

    except Exception as e:
        await message.reply_text("I don't have admin rights in this group. Please promote me to admin.")
        print(f"Error: {e}")


