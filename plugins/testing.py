from pyrogram import Client, filters
from pyrogram.types import Message

ADMIN_GROUP_ID = -1002059805189

@Client.on_message(filters.private & filters.command("send"))
async def forward_message_to_group(client, message):
 try:
    text = message.text.split(" ", 1)[1] 
    user_id = message.from_user.id
    await message.forward(ADMIN_GROUP_ID)
    await client.send_message(f"{user_id}")
    await message.reply_text("Message forwarded to the admins.")
 except Exception as e:
    await message.reply_text(f"error{e}")

@Client.on_message(filters.command("reply"))
async def reply_to_forwarded_message(client, message:Message):
 try:  

    reply_text = message.text.split(" ", 1)[1] 
    await message.reply_text(f"reply send to {user_id}")
 except Exception as e:
    await message.reply_text(f"error{e}")
