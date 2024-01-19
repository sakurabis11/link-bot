import pyrogram
from pyrogram import filters, Client
from info import DATABASE_URI, DATABASE_NAME
from pymongo import MongoClient

MONGO_URI = DATABASE_URI

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
welcome_messages = db["welcome_messages"]

@Client.on_message(filters.command("welcome") & filters.chat(types=["group", "supergroup"]))
async def handle_welcome(client, message):
    args = message.command[1:]
    chat_id = message.chat.id
    user = message.from_user

    if user.status in ["creator", "administrator"]:
        if args[0] == "on":
            await welcome_messages.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
            await message.reply_text("Welcome message enabled for this group.")
        elif args[0] == "off":
            await welcome_messages.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
            await message.reply_text("Welcome message disabled for this group.")
        else:
            await message.reply_text("Invalid argument. Use /welcome on or /welcome off.")
    else:
        await message.reply_text("Only admins can manage welcome messages.")

@Client.on_message(filters.command("set_welcome") & filters.chat(types=["group", "supergroup"]))
async def handle_set_welcome(client, message):
    args = message.command[1:]
    chat_id = message.chat.id
    user = message.from_user

    if user.status in ["creator", "administrator"]:
        if len(args) > 0:
            new_message = " ".join(args)
            await welcome_messages.update_one({"chat_id": chat_id}, {"$set": {"message": new_message}}, upsert=True)
            await message.reply_text("Welcome message updated successfully!")
        else:
            await message.reply_text("Please provide a welcome message.")
    else:
        await message.reply_text("Only admins can set welcome messages.")

@Client.on_message(filters.command("show_message") & filters.chat(types=["group", "supergroup"]))
async def handle_show_message(client, message):
    chat_id = message.chat.id
    welcome_data = await welcome_messages.find_one({"chat_id": chat_id})

    if welcome_data:
        message = welcome_data.get("message")
        await message.reply_text(message)
    else:
        await message.reply_text("No welcome message set for this group.")

@Client.on_message(filters.new_chat_members)
async def handle_new_member(client, message):
    chat_id = message.chat.id
    welcome_data = await welcome_messages.find_one({"chat_id": chat_id})

    if welcome_data and welcome_data.get("enabled"):
        message = welcome_data.get("message")
        new_member = message.new_chat_members[0]
        formatted_message = message.format(
            mention=new_member.mention,
            username=new_member.username,
            first_name=new_member.first_name,
            last_name=new_member.last_name,
            user_id=new_member.id
        )
        try:
            await message.reply_text(formatted_message)
        except Exception as e:
            print(f"Error sending welcome message: {e}")


