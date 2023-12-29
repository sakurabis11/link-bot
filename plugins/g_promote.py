import pyrogram
from pyrogram import Client, filters
from pyrogram.types import *

@Client.on_message(filters.command("add") & filters.group)
async def add_admin(client, message):
    args = message.text.split(" ", 2)
    if len(args) != 2:
        await message.reply_text("Invalid command usage. Please use /add <user_id>")
        return

    user_id = int(args[1])
    try:
        await client.get_users(user_id)  # Check if user exists
    except Exception:
        await message.reply_text("Invalid user ID.")
        return

    user = await client.get_users(user_id)
    buttons = [
        InlineKeyboardButton("Yes", callback_data="promote_yes"),
        InlineKeyboardButton("No", callback_data="promote_no"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=2).add(*buttons)
    await message.reply_text(
        f"Do you want to add {user.mention} as an admin?", reply_markup=keyboard
    )

@Client.on_callback_query()
async def callback_handler(client, query):
    if query.data == "promote_yes":
        try:
            await client.promote_chat_member(
                query.message.chat.id, query.message.reply_to_message.from_user.id, can_manage_chat=True
            )
            await query.message.edit_text(f"{query.message.reply_to_message.from_user.mention} has been promoted to admin.")
        except Exception as e:
            await query.message.edit_text(f"Failed to promote: {e}")
    elif query.data == "promote_no":
        await query.message.edit_text("Promotion canceled.")
    await query.answer()

