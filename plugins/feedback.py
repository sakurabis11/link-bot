import pyrogram
from pyrogram import Client, filters
from info import LOG_CHANNEL 

@Client.on_message(filters.command("feedback"))
async def handle_feedback(client, message):
    user_feedback = message.text.split(" ", 1)[1]  

    await message.reply_text("Thank you for your feedback!")

    await client.forward_messages(
        LOG_CHANNEL,
        message.chat.id,
        message_ids=message.message_id,
        caption=f"**Feedback from {message.from_user.first_name}** (@{message.from_user.username})",
    )

