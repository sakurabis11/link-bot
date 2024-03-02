from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import requests
import os
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.command("vision") & filters.photo)
async def vision(client, message: Message):
    try:
        photo_path = await message.download_photo()

        if not os.path.exists(photo_path):
            await message.reply_text("Failed to download the photo. Please try again.")
            return


        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
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

        model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                                     generation_config=generation_config,
                                     safety_settings=safety_settings
                                     )
        image_data = {
            "mime_type": "image/jpeg",
            "data": open(photo_path, "rb").read(),
        }
        prompt_parts = ["what is the picture shows", image_data]
        response = model.generate_content(prompt_parts)
        await message.reply_text(response.text)
        os.remove(photo_path)
    except Exception as e:
        await message.reply_text(f"{e}")
