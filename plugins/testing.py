from pyrogram import Client, filters
from pyrogram.types import Message

ADMIN_GROUP_ID = -1002059805189

@Client.on_message(filters.private & filters.command("send"))
async def forward_message_to_group(client, message):
 try:
    text = message.text.split(" ", 1)[1] 
    user_id = message.from_user.id
    await message.forward(ADMIN_GROUP_ID)
    await client.send_message(ADMIN_GROUP_ID, text=f"<code>{user_id}</code>")
    await message.reply_text("Message forwarded to the admins.")
 except Exception as e:
    await message.reply_text(f"error{e}")

@Client.on_message(filters.command("reply"))
async def reply_to_forwarded_message(client, message:Message):
 try:  
    user_id = message.text.split(" ", 1)[1] 
    reply_text = message.text.split(" ", 2)[2]
    await client.send_message(user_id, text=f"Reply from my admin <code>{reply_text}</code>")
    await message.reply_text(f"reply send to {user_id}")
 except Exception as e:
    await message.reply_text(f"error{e}")
