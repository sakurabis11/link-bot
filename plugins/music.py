import os
import shutil
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def download_songs(query, randomdir):
    try:
        print(f"Downloading song: {query}")
        # Use your preferred song download method here
        music_file_path = f"{randomdir}/{query}.mp3"
        # Download the song using the provided query and save it to music_file_path
        print(f"Song downloaded: {music_file_path}")
        return music_file_path
    except Exception as e:
        print(f"Failed to download song: {e}")
        raise e

@Client.on_message(filters.command('music') & filters.text & filters.incoming)
async def song(_, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        k = await message.reply("⌛")
        print('⌛')
        try:
            randomdir = f"/tmp/{str(randint(1,100000000))}"
            os.mkdir(randomdir)
        except Exception as e:
            await message.reply_text(f"Failed to send song retry after sometime 😥 reason: {e} ")
            return await k.delete()

        query = message.text.split(None, 1)[1]
        await k.edit("downloading")
        print('downloading')
        await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)
        path = await download_songs(query,randomdir)
        await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
        await k.edit('uploading')
        await message.reply_audio(path)

    except IndexError:
        await message.reply("song requies an argument `eg /song faded`")
        return await k.delete()
    except Exception as e:
        await message.reply_text(f"Failed to send song 😥 reason: {e}")
    finally:
        try:
            shutil.rmtree(randomdir)
            await message.reply_text(f"Check out @Unni0240")
            return await k.delete()
        except:
            pass

