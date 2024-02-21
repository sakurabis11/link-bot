import asyncio
import re
from pyrogram import Client, filters
import pymongo
from info import DATABASE_URI

client = pymongo.MongoClient(DATABASE_URI)
db = client["antispam_database"]
collection = db["antispam_settings"]

link_pattern = r"https"

@Client.on_message(filters.command("antispam on") & filters.group)
async def handle_antispam_on(client, message):
    group_id = message.chat.id
    is_enabled = collection.find_one({"group_id": group_id})
    if is_enabled:
       await message.reply("Anti-spam is already enabled.")
       return

    collection.insert_one({"group_id": group_id, "enabled": True})
    await message.reply("Anti-spam enabled successfully!")

@Client.on_message(filters.command("antispam off") & filters.group)
async def handle_antispam_off(client, message):
   group_id = message.chat.id
   is_enabled = collection.find_one({"group_id": group_id})
   if not is_enabled:
      await message.reply("Anti-spam is already disabled.")
      return

   collection.find_one_and_update({"group_id": group_id}, {"$set": {"enabled": False}})
   await message.reply("Anti-spam disabled successfully!")
     
@Client.on_message(filters.text & filters.group)
async def handle_text_messages(client, message):
    group_id = message.chat.id
    is_antispam_enabled = collection.find_one({"group_id": group_id, "enabled": True})

    if message.text == link_pattern
       await message.delete()
       return         
