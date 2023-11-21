from pyrogram import Client, filters
from pyrogram.types import Message
import openai
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY

OPENAI_API_KEY = openai.api_key

@Client.on_message(filters.private & filters.text)
def chat_with_openai(client, message):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.text}
        ]
    )
    message.reply_text(response.choices[0].text)
