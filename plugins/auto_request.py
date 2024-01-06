import pyrogram
from pyrogram import Client, filters

@Client.on_chat_join_request()
async def auto_accept_request(client, chat_member_update):
    chat_id = chat_member_update.chat.id
    user_id = chat_member_update.from_user.id

    try:
        await client.get_chat_member(chat_id, client.me.id)
        await client.approve_chat_join_request(chat_id, user_id)
    except Exception as e:
        print(f"Error approving request: {e}")
