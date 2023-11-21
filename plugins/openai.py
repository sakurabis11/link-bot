import openai
from pyrogram import Client, filters
import asyncio
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, PORT

# Define GPT-3 command handler
@Client.on_message(filters.command("openai"))
async def openai_handler(client, message):
    try:
        # Get the prompt from the message
        prompt = message.text.split(" ")[1]

        # Create a completion request
        completion_request = {
            "prompt": prompt,
            "model": "text-davinci-003",
            "temperature": 0.5,
            "max_tokens": 1024,
            "top_p": 1,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }

        # Send the completion request to OpenAI
        response = await openai.Completion.create(**completion_request)

        # Extract the response text
        response_text = response["choices"][0]["text"][:2048]

        # Send the OpenAI response to the Telegram chat
        await message.reply(response_text)
    except IndexError:
        await message.reply("Please provide a prompt after the command, e.g., /openai Tell me a joke.")
    except openai.errors.OpenAIError as e:
        if e.status_code == 400:
            await message.reply("Invalid prompt or request format. Please try again.")
        else:
            await message.reply(f"OpenAI API error: {e.status_code} - {e.reason}. Please try again later.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        await message.reply("An unexpected error occurred while processing your request. Please try again later.")
