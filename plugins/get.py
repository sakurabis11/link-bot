import asyncio
from pyrogram import Client, filters
import google.generativeai as genai

# Configure Generative AI
genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

# Store image data and message IDs
image_data = {}

@Client.on_message(filters.photo)
async def handle_photo(client, message):
    image_data[message.message_id] = await client.download_media(message)
    await message.reply("Image received. Send /get followed by a query to generate a response.")

@Client.on_message(filters.command("get", prefixes="/"))
async def handle_query(client, message):
    if message.reply_to_message and message.reply_to_message.message_id in image_data:
        query = message.text.split(" ", 1)[1]
model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config={
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    },
    safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ],
)

        prompt_parts = [query]
        image_parts = [{"content": image_data[message.reply_to_message.message_id]}]
        response = model.generate_content(prompt_parts, image_parts=image_parts)
        await message.reply(response.text)
        del image_data[message.reply_to_message.message_id]  # Clear image data
    else:
        await message.reply("Please reply to an image with /get {query}")


