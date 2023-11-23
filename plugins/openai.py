from pyrogram import Client, filters
from pyrogram.types import Message
import openai
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, PORT

openai.api_key = OPENAI_API_KEY

@Client.on_message(filters.command("openai"))
async def openai_command(client, message):
  try:
    user_input = message.text

    if "when user" in user_input:
      await message.reply_text("I am ready to assist. Please enter a prompt or question.eg:- /openai {ur_question}")
    else:
      user_message = {
        "role": "user",
        "content": user_input
      }

      response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "I am ready to assist."},
            user_message
          ]
      )

      await message.reply_text(response.choices[0].text)

  except Exception as e:
    error_message = f"Sorry, an error occurred: {str(e)}"
    await message.reply_text(error_message)
