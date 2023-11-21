from pyrogram import Client, filters
from pyrogram.types import Message
import openai
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY

@Client.on_message(filters.command("openai"))
async def generate_response(_, message: Message):
    # Get the user's message
    user_input = message.text

    # Use OpenAI to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=100
    )

    # Send the generated response to the user
    message.reply_text(response['choices'][0]['text'])
