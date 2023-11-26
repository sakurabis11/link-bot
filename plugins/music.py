import os
import shutil
from pyrogram import filters, enums, Client
import random
from random import randint
from pyrogram import errors
import ffmpeg
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor

def download_songs(query, random_dir):
  future = Future()

  def download_song_async():
    try:
      audio_path = os.path.join(random_dir, "downloaded_song.mp3")

      future.set_result(audio_path)
    except Exception as e:
      future.set_exception(e)

  executor = ThreadPoolExecutor(max_workers=1)
  executor.submit(download_song_async)

  return future

@Client.on_message(filters.command('music') & filters.text)
async def song(_, message):
  try:
    await message.reply_chat_action(enums.ChatAction.TYPING)
    k = await message.reply("⌛️")
    print('⌛️')

    try:
      random_dir = f"/tmp/{str(random.randint(1, 100000000))}"
      os.mkdir(random_dir)
    except Exception as e:
      await message.reply_text(f"Failed to send song, retry after sometime 😥 Reason: {e}")
      return await k.delete()

    query = message.text.split(None, 1)[1]
    await k.edit("Downloading ⬇️")
    print('Downloading ⬇️')

    await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)
    audio_path_future = await download_songs(query, random_dir)

    audio_path = await audio_path_future.result()

    if audio_path_future.exception():
      await message.reply_text(f"Failed to send song 😥 Reason: {audio_path_future.exception()}")
      return await k.delete()

    await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
    await k.edit('Uploading ⬆️')

    await message.reply_audio(audio_path)

  except IndexError:
    await message.reply("Song requires an argument, e.g., /song faded")
    return await k.delete()

  except Exception as e:
    await message.reply_text(f"Failed to send song 😥 Reason: {e}")

  finally:
    try:
      shutil.rmtree(random_dir)
      await message.reply_text("chumma")
      return await k.delete()
    except:
      pass
