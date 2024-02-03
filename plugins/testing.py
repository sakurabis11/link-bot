# It is not a professional code, it is a basic idea from the mrtg brain.
# Don't laugh, when u see this code, please!

from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS
import asyncio

ADMIN_GROUP_ID = -1002059805189

@Client.on_message(filters.private & filters.command("send"))
async def forward_message_to_group(client, message):
 try:
    text = message.text.split(" ", 1)[1] 
    user_id = message.from_user.id
    await message.forward(ADMIN_GROUP_ID)
    await client.send_message(ADMIN_GROUP_ID, text=f"ᴜꜱᴇʀ-ɪᴅ= <code>{user_id}</code>")
    success_message = await message.reply_text("Message forwarded to the admins.")
    await asyncio.sleep(10)
    await success_message.delete()
    
 except Exception as e:
    await message.reply_text(f"error{e}")

@Client.on_message(filters.command("reply") & filters.user(ADMINS) & filters.chat(int(ADMIN_GROUP_ID)) & filters.reply)
async def reply_to_forwarded_message(client, message: Message):
    try:
        if message.reply_to_message and message.reply_to_message.forward_from:
            msg_id = message.reply_to_message.forward_from.id
            reply_t = message.text.split(" ", 1)[1] 
            await client.send_message(msg_id, reply_t)
            await message.reply_text(f"sucessfully sended to <a href='tg://user?id={msg_id}'><b>ᴄʟɪᴄᴋ ʜᴇʀᴇ</b></a>")    
        else:
            await message.reply_text(f"Reply the forward message or Use this command: <code>!reply <user_id> <reply_message>")
    except Exception as e:
            await message.reply_text(f"An error occurred: {e}\n\nIf there is an error then use this command: <code>!ans <user_id> <reply_message>")



