import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message

WELCOME_MESSAGE = (
    f"ʜɪ {from_user.mention}, ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ɪs ᴀᴄᴄᴘᴇᴛᴇᴅ "
)  # Access Message class here

@Client.on_chat_join_request(filters.chat_member(new_chat_members=True))
async def auto_accept(client, message: Message):  # Specify Message type
    chat = message.chat
    user = message.from_user
    for new_member in message.new_chat_members:
        if not new_member.is_self:
            await client.approve_chat_join_request(chat.id, new_member.id)
            await client.send_message(chat_id=new_member.id, text=WELCOME_MESSAGE)
