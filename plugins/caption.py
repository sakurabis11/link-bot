from pyrogram import Client, filters

NEW_CAPTION = "this is working.."

@Client.on_message(filters.document)
async def handle_document(client, message):
  chat_id = message.chat.id
  if chat_id < 0:
     try:
        await client.edit_message_caption(
             chat_id=chat_id,
              message_id=message.message_id,
              caption=NEW_CAPTION,
        )
     except Exception as e:
        await message.reply_text(f"Error editing caption: {e}")


