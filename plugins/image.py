import pyrogram
import openai
from pyrogram import Client, filters

OPENAI_API_KEY = "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"

@Client.on_message(filters.command(["image"]))
async def generate_image(client, message):
    prompt = message.text.split(" ", 1)[1]

    try:
        # Correctly use the context manager and access the images.generate method
        with openai(api_key=OPENAI_API_KEY) as api:
            response = api.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="1024x1024",
                quality="hd",
                n=1,
            )
            image_url = response.data[0].url

            await message.reply_photo(image_url, caption=f"Here's the generated image based on your prompt: {prompt}")
    except Exception as e:
        await message.reply_text(f"Error generating image: {e}")
