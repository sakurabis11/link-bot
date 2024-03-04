from pyrogram import Client, filters
from pyrogram.types import Message
from database.users_db import db

@Client.on_message(filters.group & filters.command('set_caption'))
async def add_caption(client, message: Message):
 try:
    if len(message.command) == 1:
       return await message.reply_text("**Give The Caption\n\nExample :- `/set_caption 📕Name ➠ : {filename} \n\n🔗 Size ➠ : {filesize} \n\n⏰ Duration ➠ : {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await db.set_caption(message.chat.id, caption=caption)
    await message.reply_text("**Your Caption Successfully Added ✅**")
 except Exception as e:
    await message.reply_text(f"{e}")

@Client.on_message(filters.group & filters.command('del_caption'))
async def delete_caption(client, message: Message):
 try:
    caption = await db.get_caption(message.chat.id)  
    if not caption:
       return await message.reply_text("**You Don't Have Any Caption ❌**")
    await db.set_caption(message.chat.id, caption=None)
    await message.reply_text("**Your Caption Successfully Deleted 🗑️**")
 except Exception as e:
    await message.reply_text(f"{e}")
                                       
@Client.on_message(filters.group & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message: Message):
 try: 
    caption = await db.get_caption(message.chat.id)  
    if caption:
       await message.reply_text(f"**Your Caption :**\n\n`{caption}`")
    else:
       await message.reply_text("**You Don't Have Any Caption ❌**")
 except Exception as e:
    await message.reply_text(f"{e}")
