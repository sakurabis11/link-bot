import pyrogram
import openai
from pyrogram import Client, filters


OPENAI_API_KEY = "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"

bot = openai(api_key=OPENAI_API_KEY)

@Client.on_message(filters.command(["image"]))
async def generate_image(client, message):
    prompt = message.text.split(" ", 1)[1]  

    try:
        response = bot.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        await message.reply_photo(image_url, caption="Here's the generated image based on your prompt:")
    except Exception as e:
        await message.reply_text(f"Error generating image: {e}")


