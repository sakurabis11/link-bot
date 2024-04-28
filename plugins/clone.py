import pyrogram
from pyrogram import Client, filters, enums
import requests as re
import os
from database.users_db import db
from info import API_ID, API_HASH, LOG_CHANNEL

@Client.on_message(filters.command('clone') & filters.private)
async def clone_handler(client, message):
        await message.reply_text("Gᴏ ᴛᴏ @BotFather ᴀɴᴅ ᴄʀᴇᴀᴛᴇ ᴀ ɴᴇᴡ ʙᴏᴛ.\n\nsᴇɴᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴡɪᴛʜ ᴄᴏᴍᴍᴀɴᴅ /add .(ᴇɢ:- /add 𝟷𝟸𝟹𝟺𝟻𝟼:ᴊʙᴅᴋʜsʜᴅᴠᴄʜᴊʜᴅʙʜs-sʜʙ)")

@Client.on_message(filters.command('add') & filters.private)
async def add_handler(client, message):
  try:
    new_message = message.text.split()[1:]
    bot_token = " ".join(new_message)

    if bot_tok == bot_token:
      return await message.reply("ᴏᴏᴘs! ᴛʜɪs ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ...")
    a = await message.reply_text("ᴄʟᴏɴɪɴɢ sᴛᴀʀᴛᴇᴅ")
    c_bot = Client(
      name=bot_token ,
      api_id=API_ID ,
      api_hash=API_HASH ,
      bot_token=bot_token ,
      plugins={"root": "c_plugins"}
    )
    try:
      await c_bot.start()  
      mine = await c_bot.get_me()
      await db.add_bot(message.from_user.id, message.from_user.first_name, mine.id, bot_token, mine.username)
    except Exception as e:
      await a.edit("ᴄʟᴏɴɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ")
      await message.reply_text(f'Error - <code>{e}</code>')
      return
  except Exception as e:
    await message.reply_text(e)
