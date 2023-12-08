import pyrogram
from pyrogram import Client, filters
from pymongo import MongoClient
from database.users_db import db
from info import DATABASE_NAME, DATABASE_URI
import psutil

@Client.on_message(filters.command(["stats"]))
async def stats(client, message):

  client = MongoClient(DATABASE_URI)
  db = client[DATABASE_NAME]

  user_count = await db.users.count_documents({})
  free_space = psutil.disk_usage('/').free
  db_stats = await db.command("dbStats")
  db_size = db_stats['dataSize']

  await message.reply(f"**Stats:**\n\n"
                       f"Users: {user_count}\n"
                       f"Free Space: {free_space / 1024 ** 3:.2f} GB\n"
                       f"Mongo Space: {db_size / 1024 ** 3:.2f} GB")
