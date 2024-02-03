from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS

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

@Client.on_message(filters.command("reply") & filters.user(ADMINS) & filters.chat(int(ADMIN_GROUP_ID)) & filters.reply)
async def reply_to_forwarded_message(client, message):
 try: 
    mrtg = message.text.split(" ", 1)[1]
    user_id = message.reply_to_message.forward_from_user.id
    await message.reply_text(f"{user_id}")
    await client.send_message(user_id, mrtg)
    await message.reply_text(f"reply to {user_id} sended")
 except Exception as e:
    await message.reply_text(f"error{e}")
