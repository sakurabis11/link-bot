from pyrogram import Client, filters 
import asyncio
from pyrogram.types import * 
from info import ADMINS, ADMIN_CHANNEL_ID

@Client.on_message(filters.private & filters.command("send"))
async def forward_query(client, message:Message):
 try:
    query = message.text.split(" ", 1)[1] 
    await client.send_messages(ADMIN_CHANNEL_ID, text=f"ғʀᴏᴍ {message.from_user.mention}\n\n{query}")
    await message.reply_text("Your query has been forwarded to the admin.")
 except Exception as e:
    await message.reply_text(f"{e}")
