import asyncio
from pyrogram import Client, filters

API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWE2NzM0NWQtYTQ5Zi00MTNiLTlmNWQtY2VkYzAyMGViYzczIiwidHlwZSI6ImFwaV90b2tlbiJ9.yAUteQib-6jcYVBTKtOMwWOLq-wuVu--qPOYVX6PuJE"

@Client.on_message(filters.command("imagine"))
async def imagine(client, message):
    query = message.text.split()[1:]  
    if not query:
        await message.reply_text("Please provide a prompt for the image generation.")
        return

    edenai_client = edenaiapi.Client(api_key=API_TOKEN)
    try:
        response = await edenai_client.image_generate(
            prompt=" ".join(query),
            response_as_dict=True,
            attributes_as_list=False,
            show_original_response=False,
            resolution="256x256",
            num_images=1
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
        return

    image_url = response["data"][0]["image_url"]

    await message.reply_photo(image_url)
