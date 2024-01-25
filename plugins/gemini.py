import pyrogram
from pyrogram import Client, filters  # Add the filters import
import google.generativeai as genai

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.photo & filters.command("gemini"))
async def handle_photo_and_query(client, message):
    try:
        photo = await message.download(file_name="received_photo.jpg")
        query = message.text.split(" ", 1)[1]

        if not query:
            await message.reply_text("Please provide your question after /gemini")
            return

        query = " ".join(query)
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
            safety_settings=safety_settings,
        )
        prompt_parts = [
            f"Photo: {photo.file_path}",
            f"Query: {query}",
        ]
        response = model.generate_content(prompt_parts)

        await message.reply_text(response.text)  

    except Exception as e:
        await message.reply_text(f"Error generating response: {e}")
