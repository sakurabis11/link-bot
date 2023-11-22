from pyrogram import Client, filters
from pyrogram.types import Message
import openai
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY

@Client.on_message(filters.command("gpt"))
async def gpt(client, message):
    response = openai.Completion.create(
        model="text-davinci-003",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        persence_penalty=0.0
    )
    await message.reply_text(response.choices[0].text)


