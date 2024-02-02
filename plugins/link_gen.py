from pyrogram import Client, filters

@Client.on_message(filters.command("c_id"))
async def create_link(client, message):
    chat_id = message.text.split(" ", 1)[1] 
    try:
        chat = await client.get_chat(chat_id)
        link = await client.create_chat_invite_link(chat.id)
        await message.reply_text(f"Here's the link for {chat.title}:\n{link}")
    except Exception as e:
        await message.reply_text(f"Error creating link: {e}")


