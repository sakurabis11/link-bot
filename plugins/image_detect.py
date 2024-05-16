from pyrogram import Client, filters
import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@CLient.on_message(filters.command("pic"))
async def ai_generate_private(client , message):
 try:
    replied = message.reply_to_message
    if not replied:
        return await message.reply_text("Ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ")
    if not replied.photo:
        return await message.reply_text("ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴀ ᴠᴀʟɪᴅ ᴍᴇᴅɪᴀ")
    text = await message.reply_text("<code>detecting...</code>")
    media = await replied.download()

    generation_config = {
        "temperature": 1 ,
        "top_p": 0.95 ,
        "top_k": 64 ,
        "max_output_tokens": 8192 ,
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT" ,
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        } ,
        {
            "category": "HARM_CATEGORY_HATE_SPEECH" ,
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        } ,
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT" ,
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        } ,
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT" ,
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        } ,
    ]
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest" ,
                                  generation_config=generation_config ,
                                  safety_settings=safety_settings)
   x = text.edit("w8...")

    prompt_parts = [
        "input: " ,
        genai.upload_file(f"<path>{media}") ,
        " what is this picture shows" ,
        "output: " ,
    ]

    response = model.generate_content(prompt_parts)
    await message.reply_text(prompt_parts)
    os.remove(media)
 except Exception as e:
    await message.reply_text(e)
