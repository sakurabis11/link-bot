from pyrogram import filters, Client
from pyrogram.types import InlineQueryResultArticle, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_inline_query()
async def handle_inline_query(client, query):
  search_query = query.query.lower()
  if search_query.startswith("owner"):
    results = [
         InlineQueryResultArticle(
           title= "Dᴇᴠᴇʟᴏᴩᴇʀ: <a href='https://t.me/MrTG_Coder'>ᴍʀ.ʙᴏᴛ ᴛɢ</a>",
           thumb_url="https://telegra.ph/file/683258036c3245d6ee95e.jpg"
         )
    ]
    await query.answer(results)
