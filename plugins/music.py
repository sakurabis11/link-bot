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
    # Download the song using a music downloader library or API
    # Save the downloaded song file to the temporary directory

    # Create a Future object to store the result of the download operation
    future = Future()

    # Start a separate thread to perform the download operation
    def download_song_async():
        try:
            # Download the song and save it to the temporary directory
            audio_path = os.path.join(random_dir, "downloaded_song.mp3")
            # ...

            # Set the result of the download operation to the Future object
            future.set_result(audio_path)
        except Exception as e:
            # Set an exception to the Future object if an error occurs
            future.set_exception(e)

    # Start the download operation in a separate thread
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(download_song_async)

    # Return the Future object to the caller
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

        # Wait for the download operation to complete
        audio_path = await audio_path_future

        # Check if there was an error during the download operation
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
            await message.reply_text("Check out new update")
            return await k.delete()
        except:
            pass

