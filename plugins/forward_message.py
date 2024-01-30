from pyrogram import Client, filters 
import asyncio
from pyrogram.types import * 
from info import ADMINS, ADMIN_CHANNEL_ID

@Client.on_message(filters.private & filters.command("send"))
async def forward_query(client, message:Message):
    query = message.text.split(" ", 1)[1] 
    await client.send_messages(ADMIN_CHANNEL_ID, text=f"ғʀᴏᴍ {message.from_user.mention}\n\n{query}")
    await message.reply_text("Your query has been forwarded to the admin.")

@Client.on_message(filters.chat(int(ADMIN_CHANNEL_ID)) & filters.command("reply") & filters.user(ADMINS))
async def send_answer(client, message):
    answer = message.text.split(" ", 1)[1]  
    reply_to_message = await client.get_messages(ADMIN_CHANNEL_ID, message.reply_to_message.message_id)
    user_id = reply_to_message.forward_from.id
    await client.send_message(user_id, answer)
