from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from info import REQUESTED_CHANNEL
import google.generativeai as genai

genai.configure(api_key="AIzaSyD214hhYJ-xf8rfaWX044_g1VEBQ0ua55Q")

@Client.on_message(filters.command("ai"))
async def ai_generate(client, message):
    user_input = message.text.split()[1:]

    if not user_input:
        await message.reply_text("Please provide your question after /ask")
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
