import pyrogram
from pyrogram import Client, filters
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="AIzaSyDzq1pXw1-9JS7Z1fQ0m1RGdHK6vRY9I7Q")

@Client.on_message(filters.photo & filters.reply & filters.command(["ask"]))
async def handle_image_prompt(client, message):
    # Retrieve image
    image_file = await message.download()

    # Get user prompt
    user_input = message.text.split()[1:]
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
    # ... other safety settings
]
model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


    # Prepare image and prompt
    image_parts = [{"mime_type": "image/jpeg", "data": open(image_file, "rb").read()}]
    prompt_parts = [user_prompt, image_parts[0]]

    # Generate response
    response = model.generate_content(prompt_parts)

    # Send response to user
    await message.reply_text(response.text)


