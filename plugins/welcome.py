import pyrogram
from pyrogram import filters, Client
import motor.motor_asyncio
from info import DATABASE_URI

MONGO_URI = DATABASE_URI

db = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI).welcome_bot

async def admin_check(client, message):
    """Checks if the user is an admin in the group."""
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ["creator", "administrator"]

@client.on_message(filters.command("welcome") & filters.group)
async def toggle_welcome(client, message):
    """Toggles the welcome message on or off."""
    if await admin_check(client, message):
        action = message.command[1].lower()
        chat_id = message.chat.id

        if action in ["on", "off"]:
            await db.welcome_settings.update_one(
                {"chat_id": chat_id},
                {"$set": {"welcome_enabled": action == "on"}},
                upsert=True  # Create the document if it doesn't exist
            )
            await message.reply_text(f"Welcome message is now {action} in this group.")
        else:
            await message.reply_text("Invalid action. Use /welcome on or /welcome off.")

@client.on_message(filters.new_chat_members)
async def welcome_new_members(client, message):
    """Welcomes new members if the feature is enabled."""
    chat_id = message.chat.id
    welcome_enabled = await db.welcome_settings.find_one({"chat_id": chat_id})
    if welcome_enabled and welcome_enabled["welcome_enabled"]:
        for new_member in message.new_chat_members:
            await message.reply_text(f"Welcome, {new_member.mention}! ")


