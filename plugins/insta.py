from pyrogram import Client, filters

@Client.on_message(filters.command("insta"))
async def handle_insta_command(client, message):
    # Check if there is text after the command
    if len(message.text) == 5:
        message.reply_text("Please provide an Instagram Reels link after the /insta command.")
        return

    # Extract the text after the command
    insta_link = message.text[5:]

    # Check if the link starts with "https://www.instagram.com/reel/"
    if not insta_link.startswith("https://www.instagram.com/reel/"):
        message.reply_text("Invalid Instagram Reels link. Please provide a proper link.")
        return

    # Extract the Reels ID after "reel/"
    reels_id = insta_link[len("https://www.instagram.com/reel/"):]

    # Reply with the extracted Reels ID
    message.reply_text(f"https://www.ddinstagram.com/reel/{reels_id}")
