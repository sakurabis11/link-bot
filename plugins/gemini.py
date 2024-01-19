import pyrogram
from pyrogram import Client, filters
import google.generativeai as genai

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.command("gemini") & filters.photo)
async def generate_caption(client, message):
    image_path = await message.download_media()  
    user_input = message.text.split()[1:]
    query = " ".join(user_input)

    if not message.reply_to_message:  
        await message.reply_text("Please reply to a photo.")
        return

    # Generation and safety settings
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

    image_parts = [image_path]
    prompt_parts = [query, image_parts[0]]

    response = model.generate_content(prompt_parts)
    await message.reply_text(response.text)
