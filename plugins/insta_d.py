import pyrogram
from pyrogram import Client, filters

@Client.on_message(filters.command("reel"))
async def extract_reel_link(client, message):
    link = message.text.split(" ")[1]  # Extract the link from the command

    if "https://www.instagram.com/reel/" in link:
        reel_id = link.replace("https://www.instagram.com/reel/", "").split("reel/")[0]  # Extract the reel ID
        await message.reply_text(f"Reel ID: {reel_id}")  # Send the extracted reel ID to the user
    else:
        await message.reply_text("Invalid link format. Please provide a valid Instagram reel link.")

