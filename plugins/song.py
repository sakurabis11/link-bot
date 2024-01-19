import os
import random
import shutil
from pyrogram import Client, filters, enums
from yt_dlp import YoutubeDL

async def download_songs(query, download_directory="."):
    query = f"{query} Lyrics".replace(":", "").replace("\"", "")
    ydl_opts = {
        "format": "bestaudio/best",
        "default_search": "ytsearch",
        "noplaylist": True,
        "nocheckcertificate": True,
        "outtmpl": f"{download_directory}/%(title)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]["id"]
            info = ydl.extract_info(video)
            filename = ydl.prepare_filename(info)
            if not filename:
                print(f"Track Not Found⚠️")
            else:
                path_link = filename
                return path_link
        except Exception as e:
            pass
            print(e)
    return video

@Client.on_message(filters.command("song"))
async def song(_, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        k = await message.reply("⌛")
        print("⌛")
        try:
            randomdir = f"/tmp/{str(random.randint(1, 100000000))}"
            os.mkdir(randomdir)
        except Exception as e:
            await message.reply_text(f"Failed to send song retry after sometime  reason: {e}")
            return await k.delete()
        query = message.text.split(None, 1)[1]
        await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)
        path = await download_songs(query, randomdir)
        await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
        await k.edit("uploading")
        await message.reply_audio(path)

    except IndexError:
        await message.reply("song requires an argument `eg /song lover`")
        return await k.delete()
    except Exception as e:
        await message.reply_text(f"Failed to send song  reason: {e}")
    finally:
        try:
            shutil.rmtree(randomdir)
            return await k.delete()
        except:
            pass
