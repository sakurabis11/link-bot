from pyrogram import Client, filters

@Client.on_message(filters.document & filters.private)
async def document_handler(client, message):
    await message.reply(message.document.file_id)
    await message.reply_text(f"https://t.me/mrtgcoderbot?start={message.document.file_id}")
