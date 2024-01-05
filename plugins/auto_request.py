import pyrogram
from pyrogram import Client, filters

@Client.on_message(filters.chat_member(new_chat_members=True))
async def auto_accept(client, message):
    WELCOME_MESSAGE = f"ʜɪ {message.from_user.mention}, ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ɪs ᴀᴄᴄᴘᴇᴛᴇᴅ "

    for new_member in message.new_chat_members:
        if not new_member.is_self:
            await client.approve_chat_join_request(message.chat.id, new_member.id)
            await client.send_message(chat_id=new_member.id, text=WELCOME_MESSAGE)
