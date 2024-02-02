from pyrogram import Client, filters

ADMIN_GROUP_ID = -1002059805189

@Client.on_message(filters.private & filters.command("send"))
async def forward_message_to_group(client, message):
 try:
    text = message.text.split(" ", 1)[1] 
    await message.forward(ADMIN_GROUP_ID)
    await message.reply_text("Message forwarded to the admins.")
 except Exception as e
    await message.reply_text(f"error{e}")

@Client.on_message(filters.command("reply"))
async def reply_to_forwarded_message(client, message):
 try:  
    reply_text = message.text.split(" ", 1)[1] 
    await message.reply_to_message.forward(message.reply_to_message.from_user.id)
    await app.send_message(message.reply_to_message.from_user.id, reply_text)
 except Exception as e
    await message.reply_text(f"error{e}")
