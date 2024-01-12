import pyrogram
from pyrogram import Client, filters
import google.generativeai as genai

genai.configure(api_key="AIzaSyDzq1pXw1-9JS7Z1fQ0m1RGdHK6vRY9I7Q")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [...]  
model = genai.GenerativeModel(model_name="gemini-pro",
                             generation_config=generation_config,
                             safety_settings=safety_settings)



@Client.on_message(filters.command(["ai"]))
async def handle_ai_command(client, message):
    user_input = message.text.split()[1:]  
    user_input = " ".join(user_input)  

    convo = model.start_chat(history=[
        {"role": "user", "parts": [""]},
        {"role": "model", "parts": [""]}
    ])
    convo.send_message(user_input)
    ai_response = convo.last.text

    await message.reply_text(ai_response)  


