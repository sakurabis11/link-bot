import pyrogram
import re
from pyrogram import Client, filters

@Client.on_message(filters.regex(r"https://www\.instagram\.com/reel/(.*)"))
async def extract_reel_link(client, message):
    link = message.text

    if "https://www.instagram.com/reel/" in link:
        reel_id = link.replace("https://www.instagram.com/reel/", "").split("reel/")[0]
        reels = f"<a href='https://www.ddinstagram.com/reel/{reel_id}'>https://www.instagram.com/reel/{reel_id}</a>"
        await message.reply_text(f"{reels}", disable_web_page_preview=True)
    else:
        await message.reply_text("Invalid link format. Please provide a valid Instagram reel link.")
