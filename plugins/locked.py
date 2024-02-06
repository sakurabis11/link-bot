import pyrogram
from pyrogram import filters, Client, enums
import pymongo
from info import DATABASE_NAME, DATABASE_URI

# Connect to MongoDB
client = pymongo.MongoClient(DATABASE_URI)  
db = client[DATABASE_NAME]
collection = db["locks"]  

@Client.on_message(filters.command(["lock", "unlock", "seelocks"]) & filters.group)
async def admin_commands(client, message):
    chat_id = message.chat.id
    command = message.command[0]
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
      raise PermissionError("You are not allowed to use this command")

    if command == "lock":
      try:
        lock_type = message.text.split()[1].lower()
        collection.insert_one({"chat_id": chat_id, "type": lock_type})
        await message.reply_text(f"{lock_type} has been locked in this group.")
      except Exception as e:
        await message.reply_text(f"{e}")
          
    elif command == "unlock":
        lock_type = message.text.split()[1].lower()
        result = collection.delete_one({"chat_id": chat_id, "type": lock_type})
        if result.deleted_count:
            await message.reply_text(f"{lock_type} has been unlocked in this group.")
        else:
            await message.reply_text(f"{lock_type} is not locked in this group.")

    elif command == "seelocks":
        locks = list(collection.find({"chat_id": chat_id}))
        if locks:
            lock_types = [lock["type"] for lock in locks]
            await message.reply_text("Locked types in this group: {}".format(", ".join(lock_types)))
        else:
            await message.reply_text("There are no locked types in this group.")

# Handler for deleting locked content
@Client.on_message(filters.group)
async def delete_locked_content(client, message):
    chat_id = message.chat.id
    lock = collection.find_one({"chat_id": chat_id, "type": message.text.split()[0].lower()})
    if lock:
        await message.delete()
        await message.reply_text("{} is locked in this group.".format(lock["type"]))
