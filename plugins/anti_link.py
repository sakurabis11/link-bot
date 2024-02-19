from pyrogram import Client, filters, enums
from pymongo import MongoClient
from info import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME

client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
linked_chats = db[COLLECTION_NAME]

@Client.on_message(filters.command("antilink") & filters.group)
async def antilink(client, message):
    chat_id = message.chat.id
    command = message.text.split()[1]
    if command == "on":
        if chat_id in linked_chats:
            await message.reply_text("anti-link is already on")
        else:
            linked_chats.insert_one({"chat_id": chat_id, "enabled": True})
            await message.reply_text("Anti-link is now enabled.")
    if command == "off":
        if chat_id not in linked_chats:
            await message.reply_text("anti-link is already off")
        else:
            linked_chats.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}})
            await message.reply_text("Anti-link is now disabled.")
    else:
        await message.reply_text("Invalid command. Use /antilink on or /antilink off")

@Client.on_message(filters.text & filters.group)
async def link(client, message):
  try:
    msg = message.text
    chat_id = message.chat.id
    if chat_id in linked_chats:
       if linked_chats.find_one({"chat_id": chat_id})["enabled"]:
          if "https" in msg or "t.me/" in msg:
              await msg.delete()
              await message.reply_text("Links are not allowed in this group")
          else:
              pass
       else:
          pass 
  except Exception as e:
    await message.reply_text(f"{e}")
                  
