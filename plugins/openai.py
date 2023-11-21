import openai
from pyrogram import Client, filters
import asyncio
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, PORT

# Define GPT-3 command handler
@Client.on_message(filters.command("gpt3"))
async def gpt3_handler(client, message):
    try:
        # Extract prompt from message
        prompt = message.text.split("gpt3 ")[1]

        # Send prompt to OpenAI API and get response
        response = openai.Completion.create(
            prompt=prompt,
            model="text-davinci-003",
            temperature=0.7,
            max_tokens=1024
        )

        # Truncate response to a reasonable length
        response_text = response["choices"][0]["text"][:2048]

        # Send OpenAI response to Telegram chat
        await message.reply(response_text)

    except IndexError:
        await message.reply("Please provide a prompt after the command, e.g., /gpt3 Tell me a joke.")

    except Exception as e:
        if isinstance(e, openai.errors.OpenAIError) and e.status_code == 400:
            await message.reply("Invalid prompt or request format. Please try again.")
        elif isinstance(e, openai.errors.OpenAIError):
            await message.reply(f"OpenAI API error: {e.status_code} - {e.reason}. Please try again later.")
        else:
            print(f"Unexpected error occurred: {e}")
            await message.reply("An unexpected error occurred while processing your request. Please try again later.")

