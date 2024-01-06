import asyncio
import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from pyrogram.types import Message

@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"**𝙵𝙸𝙽𝙳𝙸𝙽𝙶 𝚈𝙾𝚄𝚁 𝚅𝙸𝙳𝙴𝙾** `{urlissed}`"
    )
    if not urlissed:
        await pablo.edit("Invalid Command Syntax Please Check help Menu To Know More!")
        return

    # Use yt-dlp for video searching and downloading
    ydl_opts = {
        "format": "best",  # Adjust format options as needed
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(urlissed, download=True)
        except Exception as e:
            await pablo.edit(f"**Download Failed! Please Try Again.**\n**Error:** `{str(e)}`")
            return

    file_stark = f"{info['id']}.mp4"
    capy = f"""
**𝚃𝙸𝚃𝙻𝙴 :** [{info['title']}]({info['webpage_url']})
**𝚁𝙴𝚀𝚄𝙴𝚂𝚃𝙴𝙳 𝙱𝚈 :** {message.from_user.mention}
**@ᴄᴄᴏᴍ_ᴛᴇᴀᴍ**
"""
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(info['duration']),
        file_name=info['title'],
        thumb=info.get('thumbnail', None),  # Use thumbnail from yt-dlp if available
        caption=capy,
        supports_streaming=True,
        reply_to_message_id=message.id
    )
    await pablo.delete()
    os.remove(file_stark)  # Clean up downloaded file
