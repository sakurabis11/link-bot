import asyncio
import os 
from pyrogram import Client, filters
from info import ADMINS
from plugins.admin_check import admin_check

TG_MAX_SELECT_LEN = 100

@Client.on_message(filters.command("purge") & filters.user(ADMINS))
async def purge(client, message):
    """ purge upto the replied message """
    if message.chat.type not in (("supergroup", "channel")):
        return

    is_admin = await admin_check(message)

    if not is_admin:
        return

    status_message = await message.reply_text("...", quote=True)
    await message.delete()
    message_ids = []
    count_deleted_messages = 0

    if message.reply_to_message:
        for message_id in range(
                message.reply_to_message.message_id,
                message.message_id
        ):
            message_ids.append(message_id)

            if len(message_ids) == TG_MAX_SELECT_LEN:
                await client.delete_messages(
                        chat_id=message.chat.id,
                        message_ids=message_ids,
                        revoke=True
                )
                count_deleted_messages += len(message_ids)
                message_ids = []

        if len(message_ids) > 0:
            await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True
            )
            count_deleted_messages += len(message_ids)

    await status_message.edit_text(
        f"deleted {count_deleted_messages} messages"
    )
    await asyncio.sleep(5)
    await status_message.delete()
