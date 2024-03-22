import pyrogram
from pyrogram import Client, filters
from info import SESSION
from pyrogram.types import Message
import asyncio

@Client.on_message(filters.command("alive", prefixes="."))
async def alive_msg(client: Client, message: Message):
  try:
    sd=await client.send_photo(message.chat.id, "https://telegra.ph/file/683258036c3245d6ee95e.jpg", caption=f"ʜɪ {message.from_user.mention},\nɪ ᴀᴍ ᴀʟɪᴠᴇ,ᴅᴏɴ'ᴛ ʙᴇ sᴄᴀᴍ")
    await asyncio.sleep(30)
    await sd.delete()
  except Exception as e:
    await message.reply_text(f"{e}")
