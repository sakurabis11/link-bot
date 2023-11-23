from pyrogram import Client, filters
import openai
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, PORT

openai.api_key = OPENAI_API_KEY

@Client.on_message(filters.command("openai"))
async def openai_command(client, message):
    try:
        user_input = message.text

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=1024,
            temperature=0  # Set temperature to 0 for deterministic output (optional)
        )

        embedding = response.choices[0].embedding
        # Now you can use the 'embedding' for further processing or analysis

        await message.reply_text(f"Text Embedding: {embedding}")

    except Exception as e:
        error_message = f"Sorry, an error occurred: {str(e)}"
        await message.reply_text(error_message)
