from pyrogram import Client, filters
from pyrogram.types import Message
import openai
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, PORT

openai.api_key = OPENAI_API_KEY  # Set the OpenAI API key

@Client.on_message(filters.command("openai"))
async def openai_command(client, message):
    try:
        # Get the text from the user's message
        user_input = message.text

        # Use OpenAI API to generate a response
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the appropriate engine
            prompt=user_input,
            max_tokens=100  # Adjust as needed
        )

        # Send the generated response back to the user
    await message.reply_text(response.choices[0].text)

    except Exception as e:
        # Handle any errors and send an error message to the user
        error_message = f"Sorry, an error occurred: {str(e)}"
  await message.reply_text(error_message)
