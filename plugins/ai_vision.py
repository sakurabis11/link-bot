from pyrogram import Client, filters
from pyrogram.types import Message
import google.generativeai as genai

@Client.on_message(filters.command("gemini"))
async def gemini(client, message: Message):
    try:

        prompt = message.text.split()[1:]
        reply_to_message = message.reply_to_message
        if reply_to_message.photo:
            image = reply_to_message.photo
        else:
            await message.reply_text("Please reply with an image and a prompt.")
            return

        try:
            pic = await client.download_media(image)
        except Exception as e:
            await message.reply_text(f"Error downloading image: {e}")
            return


        prompt = " ".join(prompt)
        prompt_parts = [pic, prompt]


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


        try:
            model = genai.GenerativeModel(
                model_name="gemini-pro-vision",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            response = model.generate_content(prompt_parts)
            await message.reply_text(response)
        except Exception as e:
            await message.reply_text(f"Error generating text: {e}")

    except Exception as e:
        await message.reply_text(f"Unexpected error: {e}")

