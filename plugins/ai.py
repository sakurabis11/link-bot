from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import requests
from info import REQUESTED_CHANNEL, SAMPLE
import google.generativeai as genai

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.command("ai") & filters.chat(SAMPLE))
async def ai_generate(client, message):
    user_input = message.text.split()[1:]

    if not user_input:
        await message.reply_text("Please provide your question after /ai")
        return

    user_input = " ".join(user_input)
  
    if user_input.lower() in ["who is your owner", "what is your owner name"]:  # Fixed indentation here
        buttons = [[
            InlineKeyboardButton("developer", url="https://t.me/sd_bots")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_sticker("CAACAgUAAxkBAAIjWGWkDiJW1Dyn6n8CjbbwxExf0FEIAAJyCgACywLBVKKgVw2dk9PbHgQ")
        await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}", reply_markup=reply_markup)
        return

    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
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
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    prompt_parts = [user_input]
    response = model.generate_content(prompt_parts)
    await message.reply_text(response.text)
    await client.send_message(REQUESTED_CHANNEL, text=f"#google_ai ʀᴇǫᴜᴇsᴛ ғʀᴏᴍ {message.from_user.mention}\nǫᴜᴇʀʏ ɪs:- {user_input}")

@Client.on_message(filters.command("ai") & filters.private)
async def ai_generate_private(client, message):
  buttons = [[
    InlineKeyboardButton("ɢʀᴏᴜᴘ", url="https://t.me/sdbots_support")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_sticker("CAACAgUAAxkBAAIjWGWkDiJW1Dyn6n8CjbbwxExf0FEIAAJyCgACywLBVKKgVw2dk9PbHgQ")
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nᴜsᴇ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪɴ ɢʀᴏᴜᴘ", reply_markup=reply_markup)

@Client.on_message(filters.command("ai") & filters.group)
async def ai_generate_group(client, message):
if message.chat.id != SAMPLE:
   buttons = [[
     InlineKeyboardButton("ɢʀᴏᴜᴘ", url="https://t.me/sdbots_support")
   ]]
   reply_markup = InlineKeyboardMarkup(buttons)
   await message.reply_sticker("CAACAgUAAxkBAAIjWGWkDiJW1Dyn6n8CjbbwxExf0FEIAAJyCgACywLBVKKgVw2dk9PbHgQ")
   await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nᴜsᴇ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪɴ ɢʀᴏᴜᴘ", reply_markup=reply_markup)
