import asyncio
from pyrogram import Client, filters
import google.generativeai as genai

# Configure Generative AI
genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.command("get", prefixes="/"))
async def handle_query(client, message):
    
    if message.reply_to_photo:
      query = message.text.split(" ", 1)[1]
        
      if not user_input:
          await message.reply_text("Please provide your question after /ai")
          return

   query = " ".join(query)  


    generation_config={
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
    
        prompt_parts = [query]
        image_parts = [{"content": image_data[message.reply_to_message.message_id]}]
        response = model.generate_content(prompt_parts, image_parts=image_parts)
        await message.reply(response.text)
    else:
        await message.reply("Please reply to an image with /get {query}")


