import pyrogram
from pyrogram import filters
import pymongo  
from info import ADMINS, DATABASE_URI

sd = pymongo.MongoClient(DATABASE_URI).db

@Client.on_message(filters.private & ~filters.user(ADMINS))  
async def handle_private_messages(client, message):
  try:
    if message.text == "/check":
        filters = list(sd.media_filters.find({}, {"filter_name": 1}))
        filter_names = [f["filter_name"] for f in filters]
        await message.reply_text("Available filters:\n" + "\n".join(filter_names))

    elif message.text.startswith("filter "):
        filter_name = message.text.split(" ")[1]
        media = sd.media_filters.find_one({"filter_name": filter_name})
        if media:
            await client.send_media(chat_id=message.chat.id, **media["media"])
        else:
            await message.reply_text("Filter not found.")
  except Exception as e:
            await message.reply_text(f"{e}")

@Client.on_message(filters.private & filters.user(ADMINS))
async def handle_admin_media(client, message):
  try:
    if message.reply_to_message and message.reply_to_message.media:
        filter_name = message.text.split(" ")[1]
        sd.media_filters.insert_one({
            "filter_name": filter_name,
            "media": message.reply_to_message.media.to_dict()
        })
        await message.reply_text("Media saved with filter: " + filter_name)
  except Exception as e:
        await message.reply_text(f"{e}")

