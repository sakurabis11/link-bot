import os
from random import randint
import shutil
import random
from pyrogram import Client, filters, enums


async def download_song(query, randomdir):
    try:
        print(f"Downloading song: {query}")
        # Use your preferred song download method here
        music_file_path = f"{randomdir}/{query}.mp3"
        # Simulating download completion
        open(music_file_path, 'w').close()
        print(f"Song downloaded: {music_file_path}")
        return music_file_path
    except Exception as e:
        print(f"Failed to download song: {e}")
        raise e

@Client.on_message(filters.command('song') & filters.text & filters.incoming)
async def song(client, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        k = await message.reply("⌛")

        try:
            randomdir = f"/tmp/{str(random.randint(1, 100000000))}"
            os.mkdir(randomdir)
        except Exception as e:
            await message.reply_text(f"Failed to send song. Retry after some time. Reason: {e}")
            return await k.delete()

        query = message.text.split(None, 1)[1].lower()
        await k.edit("Downloading...")
        print("Downloading...")
        await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)

        path = await download_song(query, randomdir)

        # Check if file exists before sending
        if not os.path.exists(path):
            await message.reply_text("Song not found.")
            return await k.delete()

        await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
        await k.edit("Uploading...")
        await message.reply_audio(path)

    except IndexError:
        await message.reply("Please provide a song name after the `/song` command.")
    except Exception as e:
        await message.reply_text(f"Failed to send song. Reason: {e}")
    finally:
        try:
            # Use a lock to prevent a race condition
            lock = client._p_lock
            with lock:
                shutil.rmtree(randomdir)
            await message.reply_text("Check out @Spotify_downloa(music) @Spotifynewss(Updates Group)")
        except Exception as e:
            print(f"Failed to cleanup temporary directory: {e}")

        # Delete the initial "Please wait" message
        await k.delete()
