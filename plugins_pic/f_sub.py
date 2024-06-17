from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import not_subscribed
import re

@Client.on_message(filters.create(not_subscribed))
async def is_not_subscribed(client, message):
    if message.text.startswith('/'): 
        buttons = [[InlineKeyboardButton(text="ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ", url="https://t.me/+5K73cpDNZAY0ZGI1")]]
        text = f"sᴏʀʀʏ {message.from_user.mention}\nʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍʏ ʙᴏᴛ."
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        return
