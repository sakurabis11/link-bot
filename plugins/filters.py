from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

@Client.on_message(filters.command("view") & filters.private)
async def view_list(client, message: Message):
  resulta = "**View List**\n\n" \
            "*<code>Love Adhura</code>\n" 
  await message.reply_text(resulta)

@Client.on_message(filters.text & filters.private)
async def text(client, message):
 try:
  msg = message.text
  msg = msg.lower()
  if msg == "love adhura":
     buttons = [[
      InlineKeyboardButton("love adhura", url=f"https://t.me/telemovieautofilterbot?start=BATCH-BQADBQAD6A0AAoHq0VePf3ny4-HMBxYE")
     ]]
     reply_markup = InlineKeyboardMarkup(buttons)
     await message.reply_text(
       text=f"{msg}",
       reply_markup=reply_markup,
       parse_mode=enums.ParseMode.HTML
     )
  else:
     pass 
 except Exception as e:
     await message.reply_text(f"Error: {e}")

