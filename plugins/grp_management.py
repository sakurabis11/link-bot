from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import *

@Client.on_message(filters.command("kick") & filters.group)
async def kick_user(client: Client, message: Message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            raise PermissionError("You are not allowed to use this command")

        replied_user = message.reply_to_message.from_user
        if not replied_user:
            raise ValueError("Please reply to the user you want to kick")

        await client.kick_chat_member(message.chat.id, replied_user.id)
        await message.reply_text("User has been kicked from this group")

    except PermissionError as e:
        await message.reply_text(str(e))
    except UserNotParticipant:
        await message.reply_text("User is not a member of this group")
    except ChatAdminRequired:
        await message.reply_text("Bot doesn't have permissions to kick members")
    except ChatWriteForbidden:
        await message.reply_text("Bot is not allowed to send messages in this group")
    except Exception as e:
        await message.reply_text("An unexpected error occurred")

@Client.on_message(filters.command("kickme") & filters.group)
async def kick_i(client: Client, message: Message):
    try:
        await client.kick_chat_member(message.chat.id, message.from_user.id)
        await message.reply_text(f"{message.user.mention} has been kicked from this group by himself/herself")

    except ChatAdminRequired:
        await message.reply_text("Bot doesn't have permissions to kick members")
    except ChatWriteForbidden:
        await message.reply_text("Bot is not allowed to send messages in this group")
    except Exception as e:
        await message.reply_text("An unexpected error occurred")
