import pyrogram
from pyrogram import Client, filters
from info import SESSION
from pyrogram.types import Message
import asyncio
import psutil
import time
import os

def format_uptime(seconds):
    days = seconds // (24*60*60)
    seconds %= (24*60*60)
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    return f"{days} days, {hours} hours, {minutes} minutes"

@Client.on_message(filters.command("alive", prefixes="."))
async def alive_msg(client: Client, message: Message):
  try:
    sd=await client.send_photo(message.chat.id, "https://telegra.ph/file/683258036c3245d6ee95e.jpg", caption=f"ʜɪ {message.from_user.mention},\nɪ ᴀᴍ ᴀʟɪᴠᴇ,ᴅᴏɴ'ᴛ ʙᴇ sᴄᴀᴍ")
    await asyncio.sleep(30)
    await sd.delete()
  except Exception as e:
    await message.reply_text(f"{e}")

@Client.on_message(filters.command("system"))
def system_info(client, message):
    uptime = format_uptime(time.time() - psutil.boot_time())
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    used_disk = psutil.disk_usage('/').percent
    used_disk_percent = psutil.disk_usage('/').percent
    client.send_message(chat_id=message.chat.id, text=f"Uᴩᴛɪᴍᴇ: <code>{uptime}</code>\nCPU Uꜱᴀɢᴇ: <code>{cpu_usage}%</code>\nRAM Uꜱᴀɢᴇ: <code>{ram_usage}%</code>\nUꜱᴇᴅ Dɪꜱᴋ: <code>{used_disk} GB </code>(<code>{used_disk_percent}%</code>)\n")
