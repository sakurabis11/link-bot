import pyrogram
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import pymongo 
from info import DATABASE_URI, DATABASE_NAME

# MongoDB setup (replace with your credentials)
client = pymongo.MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["caption_settings"]

@Client.on_message(filters.command(["caption_settings"]))
async def handle_caption_settings(client, message):
    if message.chat.type in ["group", "channel"]:
        # Check user's administrative status
        if message.from_user.status in ["creator", "administrator"]:
            markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Document ❌", callback_data="document"),
                        InlineKeyboardButton("Video ❌", callback_data="video"),
                        InlineKeyboardButton("Photos ❌", callback_data="photos"),
                    ]
                ]
            )
            await message.reply("Choose media types for custom captions:", reply_markup=markup)
        else:
            await message.reply("This command is only for group/channel admins.")

@Client.on_callback_query()
async def callback_handler(client, query):
    data = query.data
    chat_id = query.message.chat.id

    # Retrieve current settings from MongoDB
    settings = collection.find_one({"chat_id": chat_id}) or {}

    if data in ["document", "video", "photos"]:
        # Toggle setting and update button
        settings[data] = not settings.get(data, False)
        markup = await create_caption_settings_markup(settings)
        await query.edit_message_reply_markup(markup)

        # Save updated settings to MongoDB
        collection.update_one({"chat_id": chat_id}, {"$set": settings}, upsert=True)

async def create_caption_settings_markup(settings):
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"Document {'✅' if settings.get('document') else '❌'}",
                    callback_data="document",
                ),
                InlineKeyboardButton(
                    f"Video {'✅' if settings.get('video') else '❌'}",
                    callback_data="video",
                ),
                InlineKeyboardButton(
                    f"Photos {'✅' if settings.get('photos') else '❌'}",
                    callback_data="photos",
                ),
            ]
        ]
    )
    return markup


