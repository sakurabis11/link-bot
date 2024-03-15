import os, wget
import shutil
import time
from datetime import datetime
from typing import Tuple
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from info import REQUESTED_CHANNEL

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
  """run command in terminal"""
  args = cmd.split()
  process = await asyncio.create_subprocess_exec(
      *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
  )
  stdout, stderr = await process.communicate()
  return (
      stdout.decode("utf-8", "replace").strip(),
      stderr.decode("utf-8", "replace").strip(),
      process.returncode,
      process.pid,
  )

async def convert_to_audio(vid_path):
  stark_cmd = f"ffmpeg -i {vid_path} -map 0:a sd.mp3"
  _, _, returncode, _ = await runcmd(stark_cmd)
  if query == None:
      final_warner = "sd.mp3"
  elif query != None:
      final_warner = f"{query}"
  else:
      pass
  if not os.path.exists(final_warner) or returncode != 0:
      return None
  return final_warner

@Client.on_message(filters.command(["convert", "vid_to_aud"]))
async def shazam_(client, message):
  try:
      query = message.text.split(None, 1)[1]
      if not message.reply_to_message or not message.reply_to_message.video:
          return await message.reply_text("Reply to a video...")
      thumbnail = wget.download("https://telegra.ph/file/f4f20a3a7b15d588fcc2a.jpg")
      sd = await client.send_message(REQUESTED_CHANNEL, text=f"#ᴠɪᴅ_ᴛᴏ_ᴀᴜᴅ\n\nʀᴇǫᴜᴇsᴛᴇᴅ ғʀᴏᴍ {message.from_user.mention}\n\nᴀᴜᴅɪᴏ: ❌")
      stime = time.time()
      msg = await message.reply_text("Cᴏɴᴠᴇʀᴛɪɴɢ ᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪᴏ...\n\nIᴛ ᴍᴀʏ ᴄᴀᴜsᴇs sᴏᴍᴇ ᴛɪᴍᴇ ᴅᴜᴇ ᴛᴏ ᴠɪᴅᴇᴏ ᴅᴜʀᴀᴛɪᴏɴ, sᴏ ᴘʟᴇᴀsᴇ ᴡ𝟾")
      video_file = await message.reply_to_message.download()
      music_file = await convert_to_audio(video_file)
      if music_file is None:
          return await msg.edit("Fᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪo.")
      etime = time.time()
      t_k = round(etime - stime)
      await message.reply_audio(music_file, thumb=thumbnail)
      await sd.edit(f"#ᴠɪᴅ_ᴛᴏ_ᴀᴜᴅ\nʀᴇǫᴜᴇsᴛᴇᴅ ғʀᴏᴍ {message.from_user.mention}\n\nᴀᴜᴅɪᴏ: ✅\nᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪᴏ ᴄᴏɴᴠᴇʀᴛɪɴɢ ᴛɪᴍᴇ: {t_k}")
      await msg.edit(f"Cᴏɴᴠᴇʀᴛɪɴɢ ᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪᴏ...\n\nCompleted in {t_k} Seconds.")
      await asyncio.sleep(10)
      await msg.delete()
      os.remove(video_file)
      os.remove
  except Exception as e:
      await message.reply_text(f"Error: {e}")
