import pyrogram
from pyrogram import Client
from pymongo import MongoClient
from info import DATABASE_NAME, DATABASE_URI

MONGO_URI = DATABASE_URI

    client = MongoClient(MONGO_URI)
    db = client["mrtg"]

@Client.on_message(filters.command(["stats"]))
async def stats(client, message):
  
    user_count = await db.users.count_documents({})
    group_count = await db.groups.count_documents({})
    free_space = psutil.disk_usage('/').free
    db_stats = await db.command("dbStats")
    db_size = db_stats['dataSize']
    await message.reply(f"**Stats:**\n\n"
                      f"Users: {user_count}\n"
                      f"Groups: {group_count}\n"
                      f"Free Space: {free_space / 1024 ** 3:.2f} GB\n"
                      f"Mongo Space: {db_size / 1024 ** 3:.2f} GB")

