from pyrogram import Client, filters


@Client.on_message(filters.command("purge"))
async def purge(client, message):
    if message.chat.type in ["supergroup", "channel"]:
        chat_members = await client.get_chat_members(chat_id=message.chat.id)
        for member in chat_members:
            if member.user.id == client.id and member.status == "administrator":
                for message_id in range(1, message.message_id + 1):
                    try:
                        await client.delete_messages(chat_id=message.chat.id, message_ids=message_id)
                    except:
                        pass
