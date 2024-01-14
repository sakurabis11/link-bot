import enums  # Ensure enums is imported correctly
from pyrogram import Client, filters
import requests
from info import REQUESTED_CHANNEL, SAMPLE
import google.generativeai as genai

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.command("ai") & filters.chat(SAMPLE) & filters.incoming)
async def ai_generate(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if message.chat.id != SAMPLE:
            return await message.reply_text("This bot only works in the specified GROUP")

        user_input = message.text.split()[1:]

        if not user_input:
            return await message.reply_text("Please provide your question after /ai")

        user_input = " ".join(user_input)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        prompt_parts = [user_input]
        response = model.generate_content(prompt_parts)
        await message.reply_text(response.text)
        await client.send_message(REQUESTED_CHANNEL, text=f"Google request from {message.from_user.mention}\nQuery is:- {user_input}")

    elif message.chat.type in [enums.ChatType.PRIVATE]:
        await message.reply_text("This feature will only work in groups.")
