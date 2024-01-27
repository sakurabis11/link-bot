from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import *
from info import ADMINS

@Client.on_message(filters.command("promote"))
async def promote(client, message: Message):
    try:
        if message.reply_to_message is None:
            await message.reply("Please reply to the message of the user you want to promote.")
            return

        x_user = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        user_id = message.from_user.id

        user = await client.get_chat_member(chat_id, user_id)
        if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER, ADMINS):
            await message.reply("You are not an administrator in this chat.")
            return

        await client.promote_chat_member(chat_id, x_user, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True)

    except Exception as e:
        await message.reply(f"An error occurred: {e}")
