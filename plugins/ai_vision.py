from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import requests
import google.generativeai as genai

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.command("vision") & filters.reply)
async def vision(client, message: Message):
 try:
    pic = message.reply_to_message
    if not pic:
        return await message.reply_text("Reply to a photo with the /vision command.")

    media = await client.download_media(message)

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

    prompt_parts = [media,"what is the picture shows",]
    response = model.generate_content(prompt_parts)
    await message.reply_text(response.text)

 except Exception as e:
     await message.reply_text(f"{e}")
