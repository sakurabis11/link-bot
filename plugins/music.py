import os
import shutil
from pyrogram import filters, enums, Client
import random
from random import randint
from pyrogram import errors
import ffmpeg

def download_songs(query, random_dir):
    # Download the song using a music downloader library or API
    # Save the downloaded song file to the temporary directory
    # Return the path to the downloaded song file
    audio_path = os.path.join(random_dir, "downloaded_song.mp3")

    # Convert the downloaded song file to MP3 format (if necessary)
    # using ffmpeg library if the song is not in MP3 format
    if not audio_path.endswith(".mp3"):
        input_file = audio_path
        output_file = audio_path[:-4] + ".mp3"
        ffmpeg.input(input_file).output(output_file).run()

    return audio_path

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
        audio_path = await download_songs(query, random_dir)

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


