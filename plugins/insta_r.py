from pyrogram import Client, filters
from pyrogram.types import Message, Chat

# Define a message handler for any text message
@Clientt.on_message(filters.text)
async def handle_text_message(client: Client, message: Message):
    chat = message.chat
    text = message.text

    # Check if the text is an Instagram reels link
    if "https://www.instagram.com/reel/" in text:
        # Extract the reels ID from the link
        reels_id = text.split("/")[-1]

        # Edit the link to 'https://www.ddinstagram.com'
        edited_link = f"https://www.ddinstagram.com/reel/{reels_id}"

        # Send the edited link back to the user
        bot.send_message(chat.id, f"Here's the edited link: {edited_link}")
    else:
        # Reply with a message if it's not an Instagram reels link
        bot.send_message(chat.id, "Please send me an Instagram reels link.")

