import pyrogram
from pyrogram import filters, Client
from pyrogram.types import Message
from info import ADMIN_CHANNEL_ID 

@Client.on_message(filters.private & filters.command(["send"]))
async def forward_query(client, message:Message):
 try:   
    query = message.text.split(" ", 1)[1]  
    await client.forward_messages(ADMIN_CHANNEL_ID, message.chat.id, message.message_id)
    await message.reply_text("Your query has been forwarded to the admin.")
 except Exception as e
    await message.reply_text(f"{e}")    

@Client.on_message(filters.chat(int(ADMIN_CHANNEL_ID)) & filters.command(["reply"]))
async def send_answer(client, message:Message):
 try:   
    answer = message.text.split(" ", 1)[1]  
    reply_to_message = await client.get_messages(ADMIN_CHANNEL_ID, message.reply_to_message.message_id)
    user_id = reply_to_message.forward_from.id
    await client.send_message(user_id, answer)
 except Exception as e
    await message.reply_text(f"{e}")    
