from pyrogram import *
import google.generativeai as genai


# Configure Google Generative AI
genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


@Client.on_message(filters.photo & filters.reply)
async def handle_image_response(client, message):
    reply_message = message.reply_to_message

    if reply_message.photo:
        try:
            # Download the image
            photo = await client.download_media(reply_message)
            image_parts = [{"content": photo}]
            prompt_parts = []

            # Generate content using model
            response = model.generate_content(prompt_parts, image_parts=image_parts)
            await message.reply_text(response.text)
        except ModelError as e:
            await message.reply_text(f"Error generating content: {e}")
            print(f"Error: {e}")
        except Exception as e:
            await message.reply_text("Something went wrong. Please try again later.")
            print(f"Unexpected error: {e}")

