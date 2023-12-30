import os
from pyrogram import Client, filters
from info import ADMINS

feedback_dict = {}

@Client.on_message(filters.command(["feedback"]))
async def handle_feedback(client, message):
    feedback = message.text.split("/feedback ", 1)[1] 
    user_id = message.from_user.id
    feedback_dict[user_id] = feedback
    await message.reply_text("Thank you for your feedback! It has been received anonymously.")

@Client.on_message(filters.command(["view_feedback"]))
async def view_feedback(client, message):
    if message.from_user.id in ADMINS:
        if feedback_dict:
            feedback_text = "\n".join(f"{await client.get_users(user_id).first_name}: {feedback}" for user_id, feedback in feedback_dict.items())
            await message.reply_text("Here's the collected feedback:\n" + feedback_text)
        else:
            await message.reply_text("No feedback has been received yet.")
    else:
        await message.reply_text("You are not authorized to view feedback.")

