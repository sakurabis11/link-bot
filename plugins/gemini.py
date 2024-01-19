import pyrogram
from pyrogram import Client, filters
import google.generativeai as genai

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.command("gemini") & filters.photo)
async def generate_caption(client, message):
    try:
        reply_photo = message.reply_to_message.photo
        user_input = message.text.split()[1:]

        if not user_input:
            await message.reply_text("Please provide your question after /gemini")
            return

        if not reply_photo:
            await message.reply_text("Please reply to a photo with command /gemini {query}")
            return

        user_input = " ".join(user_input)

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

        model = genai.GenerativeModel(
            model_name="gemini-pro-vision",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        image_path = await message.download()
        with open(image_path, "rb") as image_file:

            prompt_parts = [user_input, image_file.read()]

            response = model.generate_content(prompt_parts)
            await message.reply_text(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")
        await message.reply_text("An error occurred. Please try again later.")
