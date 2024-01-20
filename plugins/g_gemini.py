import google.generativeai as genai
from pyrogram import filters, Client

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")  

@Client.on_message(filters.command("gemini") & filters.photo)
async def gemini(client, message):
    m = await message.reply_text("generating...")

    prompt = " ".join(message.text.split(" ", 1)[1:])  

    if not prompt:
        await message.reply_text("Please provide your question after /gemini")
        return

    image = await client.download_media()

    # Set up the model
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

    prompt_parts = [
        "what is this image shows. describe this image. create a prompt for this image",
        image[0],  
    ]

    response = model.generate_content(prompt_parts)
    await message.reply_text(response.text)
